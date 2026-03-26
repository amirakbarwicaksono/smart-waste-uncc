import pandas as pd
import os

from core.bin_control.bin_logic import open_bin
from core.utils.timestamp import get_timestamp
from core.mqtt.client import connect_mqtt, publish

LOG_FILE = "logs/transactions.csv"

# =============================
# INIT LOG FILE (tambah kolom weight_status)
# =============================
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=[
        "timestamp", "barcode", "waste_type",
        "bin_type", "bin_state", "bin_duration_sec",
        "weight_status"  # <-- KOLOM BARU
    ]).to_csv(LOG_FILE, index=False)

# =============================
# CONNECT MQTT (ONCE)
# =============================
connect_mqtt()


# =============================
# MAIN PIPELINE
# =============================
def process_waste(barcode, image, waste_type=None, bin_type=None, weight_status=None):
    """
    CENTRAL PIPELINE dengan weight_status untuk blockchain
    
    Flow:
    1. Predict (if not provided)
    2. Log OPEN dengan weight_status
    3. Publish MQTT (OPEN) dengan weight_status
    4. Open bin (simulate hardware)
    5. Log CLOSED dengan weight_status
    6. Publish MQTT (CLOSED) dengan weight_status
    """

    # =============================
    # PREDICT ONLY IF NEEDED
    # =============================
    if waste_type is None or bin_type is None:
        from core.classification.predictor import predict_image
        waste_type, bin_type = predict_image(image)

    timestamp = get_timestamp()

    # =============================
    # LOG OPEN (dengan weight_status)
    # =============================
    open_data = {
        "timestamp": timestamp,
        "barcode": barcode,
        "waste_type": waste_type,
        "bin_type": bin_type,
        "bin_state": "open",
        "bin_duration_sec": 0,
        "weight_status": weight_status  # <-- SIMPAN KE CSV
    }

    pd.DataFrame([open_data]).to_csv(
        LOG_FILE, mode='a', header=False, index=False
    )

    # =============================
    # MQTT PUBLISH (OPEN) - dengan weight_status
    # =============================
    publish(
        "smart_waste/bin",
        {
            "timestamp": timestamp,
            "barcode": barcode,
            "waste_type": waste_type,
            "bin_type": bin_type,
            "state": "open",
            "duration": 0,
            "weight_status": weight_status  # <-- KIRIM VIA MQTT
        }
    )

    # =============================
    # OPEN BIN (HARDWARE SIMULATION)
    # =============================
    bin_info = open_bin(bin_type)

    # =============================
    # LOG CLOSED (dengan weight_status)
    # =============================
    close_timestamp = get_timestamp()
    close_data = {
        "timestamp": close_timestamp,
        "barcode": barcode,
        "waste_type": waste_type,
        "bin_type": bin_type,
        "bin_state": "closed",
        "bin_duration_sec": bin_info["duration"],
        "weight_status": weight_status  # <-- SIMPAN KE CSV
    }

    pd.DataFrame([close_data]).to_csv(
        LOG_FILE, mode='a', header=False, index=False
    )

    # =============================
    # MQTT PUBLISH (CLOSED) - dengan weight_status
    # =============================
    publish(
        "smart_waste/bin",
        {
            "timestamp": close_timestamp,
            "barcode": barcode,
            "waste_type": waste_type,
            "bin_type": bin_type,
            "state": "closed",
            "duration": bin_info["duration"],
            "weight_status": weight_status  # <-- KIRIM VIA MQTT
        }
    )

    return waste_type, bin_type, bin_info["duration"]