# import pandas as pd
# import os

# from core.bin_control.bin_logic import open_bin
# from core.utils.timestamp import get_timestamp
# from core.mqtt.client import connect_mqtt, publish

# LOG_FILE = "logs/transactions.csv"

# # =============================
# # INIT LOG FILE
# # =============================
# if not os.path.exists(LOG_FILE):
#     pd.DataFrame(columns=[
#         "timestamp", "barcode", "waste_type",
#         "bin_type", "bin_state", "bin_duration_sec"
#     ]).to_csv(LOG_FILE, index=False)

# # =============================
# # CONNECT MQTT (ONCE)
# # =============================
# connect_mqtt()


# # =============================
# # MAIN PIPELINE
# # =============================
# def process_waste(barcode, image, waste_type=None, bin_type=None):
#     """
#     CENTRAL PIPELINE (Single Source of Truth)

#     Flow:
#     1. Predict (if not provided)
#     2. Log OPEN
#     3. Publish MQTT (OPEN)
#     4. Open bin (simulate hardware)
#     5. Log CLOSED
#     6. Publish MQTT (CLOSED)
#     """

#     # =============================
#     # PREDICT ONLY IF NEEDED
#     # =============================
#     if waste_type is None or bin_type is None:
#         from core.classification.predictor import predict_image
#         waste_type, bin_type = predict_image(image)

#     timestamp = get_timestamp()

#     # =============================
#     # LOG OPEN
#     # =============================
#     open_data = {
#         "timestamp": timestamp,
#         "barcode": barcode,
#         "waste_type": waste_type,
#         "bin_type": bin_type,
#         "bin_state": "open",
#         "bin_duration_sec": 0
#     }

#     pd.DataFrame([open_data]).to_csv(
#         LOG_FILE, mode='a', header=False, index=False
#     )

#     # =============================
#     # MQTT PUBLISH (OPEN)
#     # =============================
#     publish({
#         "timestamp": timestamp,
#         "barcode": barcode,
#         "waste_type": waste_type,
#         "bin_type": bin_type,
#         "state": "open",
#         "duration": 0
#     })

#     # =============================
#     # OPEN BIN (HARDWARE SIMULATION)
#     # =============================
#     bin_info = open_bin(bin_type)

#     # =============================
#     # LOG CLOSED
#     # =============================
#     close_data = {
#         "timestamp": get_timestamp(),
#         "barcode": barcode,
#         "waste_type": waste_type,
#         "bin_type": bin_type,
#         "bin_state": "closed",
#         "bin_duration_sec": bin_info["duration"]
#     }

#     pd.DataFrame([close_data]).to_csv(
#         LOG_FILE, mode='a', header=False, index=False
#     )

#     # =============================
#     # MQTT PUBLISH (CLOSED)
#     # =============================
#     publish({
#         "timestamp": close_data["timestamp"],
#         "barcode": barcode,
#         "waste_type": waste_type,
#         "bin_type": bin_type,
#         "state": "closed",
#         "duration": bin_info["duration"]
#     })

#     return waste_type, bin_type, bin_info["duration"]

# # ----------- core/pipeline/processor.py -----------
# # Tambahkan fungsi untuk handle berbagai tipe image
# def ensure_pil_image(image):
#     """Convert various image types to PIL Image"""
#     from PIL import Image
#     import io
    
#     if isinstance(image, Image.Image):
#         return image
#     elif hasattr(image, 'read'):
#         # Streamlit UploadedFile
#         image.seek(0)
#         return Image.open(image)
#     elif isinstance(image, bytes):
#         return Image.open(io.BytesIO(image))
#     elif isinstance(image, str):
#         return Image.open(image)
#     else:
#         return image

import pandas as pd
import os

from core.bin_control.bin_logic import open_bin
from core.utils.timestamp import get_timestamp
from core.mqtt.client import connect_mqtt, publish

LOG_FILE = "logs/transactions.csv"

# =============================
# INIT LOG FILE
# =============================
if not os.path.exists(LOG_FILE):
    pd.DataFrame(columns=[
        "timestamp", "barcode", "waste_type",
        "bin_type", "bin_state", "bin_duration_sec"
    ]).to_csv(LOG_FILE, index=False)

# =============================
# CONNECT MQTT (ONCE)
# =============================
connect_mqtt()


# =============================
# MAIN PIPELINE
# =============================
def process_waste(barcode, image, waste_type=None, bin_type=None):
    """
    CENTRAL PIPELINE (Single Source of Truth)

    Flow:
    1. Predict (if not provided)
    2. Log OPEN
    3. Publish MQTT (OPEN)
    4. Open bin (simulate hardware)
    5. Log CLOSED
    6. Publish MQTT (CLOSED)
    """

    # =============================
    # PREDICT ONLY IF NEEDED
    # =============================
    if waste_type is None or bin_type is None:
        from core.classification.predictor import predict_image
        waste_type, bin_type = predict_image(image)

    timestamp = get_timestamp()

    # =============================
    # LOG OPEN
    # =============================
    open_data = {
        "timestamp": timestamp,
        "barcode": barcode,
        "waste_type": waste_type,
        "bin_type": bin_type,
        "bin_state": "open",
        "bin_duration_sec": 0
    }

    pd.DataFrame([open_data]).to_csv(
        LOG_FILE, mode='a', header=False, index=False
    )

    # =============================
    # MQTT PUBLISH (OPEN) - PERBAIKAN
    # =============================
    publish(
        "smartwaste/bin/status",  # <-- TAMBAHKAN TOPIC
        {
            "timestamp": timestamp,
            "barcode": barcode,
            "waste_type": waste_type,
            "bin_type": bin_type,
            "state": "open",
            "duration": 0
        }
    )

    # =============================
    # OPEN BIN (HARDWARE SIMULATION)
    # =============================
    bin_info = open_bin(bin_type)

    # =============================
    # LOG CLOSED
    # =============================
    close_data = {
        "timestamp": get_timestamp(),
        "barcode": barcode,
        "waste_type": waste_type,
        "bin_type": bin_type,
        "bin_state": "closed",
        "bin_duration_sec": bin_info["duration"]
    }

    pd.DataFrame([close_data]).to_csv(
        LOG_FILE, mode='a', header=False, index=False
    )

    # =============================
    # MQTT PUBLISH (CLOSED) - PERBAIKAN
    # =============================
    publish(
        "smartwaste/bin/status",  # <-- TAMBAHKAN TOPIC
        {
            "timestamp": close_data["timestamp"],
            "barcode": barcode,
            "waste_type": waste_type,
            "bin_type": bin_type,
            "state": "closed",
            "duration": bin_info["duration"]
        }
    )

    return waste_type, bin_type, bin_info["duration"]