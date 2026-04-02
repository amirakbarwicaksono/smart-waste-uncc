import pandas as pd
import os
import time
import json
from datetime import datetime

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
    
    CATATAN: Fungsi ini sekarang HANYA untuk logging ke CSV.
    MQTT open/close dikirim dari user_mode dan ESP32.
    
    Flow:
    1. Predict (if not provided)
    2. Log OPEN dengan weight_status (jika ada)
    3. Open bin (simulate hardware) - OPSIONAL, untuk testing tanpa ESP32
    4. Log CLOSED dengan weight_status (jika ada)
    
    NOTE: weight_status sekarang diterima dari ESP32, bukan dari user_mode.
          Parameter weight_status disediakan untuk kompatibilitas.
    """

    # =============================
    # PREDICT ONLY IF NEEDED
    # =============================
    if waste_type is None or bin_type is None:
        from core.classification.predictor import predict_image
        waste_type, bin_type = predict_image(image)

    timestamp = get_timestamp()

    # =============================
    # LOG OPEN (dengan weight_status jika ada)
    # =============================
    open_data = {
        "timestamp": timestamp,
        "barcode": barcode,
        "waste_type": waste_type,
        "bin_type": bin_type,
        "bin_state": "open",
        "bin_duration_sec": 0,
        "weight_status": weight_status if weight_status is not None else None
    }

    pd.DataFrame([open_data]).to_csv(
        LOG_FILE, mode='a', header=False, index=False
    )

    # =============================
    # CATATAN: MQTT OPEN TIDAK DIKIRIM DARI SINI LAGI
    # MQTT open dikirim dari user_mode setelah AI predict
    # =============================

    # =============================
    # OPEN BIN (HARDWARE SIMULATION) - OPSIONAL
    # Fungsi ini hanya untuk testing tanpa ESP32
    # Untuk production dengan ESP32, bagian ini bisa di-skip
    # =============================
    # bin_info = open_bin(bin_type)
    # duration = bin_info["duration"]
    
    # Untuk sementara, gunakan duration default 30 detik
    # duration akan diupdate oleh ESP32 jika diperlukan
    duration = 30.0
    
    # =============================
    # LOG CLOSED (dengan weight_status jika ada)
    # =============================
    close_timestamp = get_timestamp()
    close_data = {
        "timestamp": close_timestamp,
        "barcode": barcode,
        "waste_type": waste_type,
        "bin_type": bin_type,
        "bin_state": "closed",
        "bin_duration_sec": duration,
        "weight_status": weight_status if weight_status is not None else None
    }

    pd.DataFrame([close_data]).to_csv(
        LOG_FILE, mode='a', header=False, index=False
    )

    # =============================
    # CATATAN: MQTT CLOSE TIDAK DIKIRIM DARI SINI LAGI
    # MQTT close dikirim dari ESP32 setelah bin tertutup
    # =============================

    return waste_type, bin_type, duration


# =============================
# ALTERNATIF: Fungsi untuk logging weight status dari ESP32
# =============================
def log_weight_status(barcode, waste_type, bin_type, weight_status, duration=0):
    """
    Log weight status ke CSV tanpa membuka bin.
    Digunakan saat menerima weight_status dari ESP32.
    """
    timestamp = get_timestamp()
    
    weight_data = {
        "timestamp": timestamp,
        "barcode": barcode,
        "waste_type": waste_type,
        "bin_type": bin_type,
        "bin_state": "weight_check",
        "bin_duration_sec": duration,
        "weight_status": weight_status
    }
    
    pd.DataFrame([weight_data]).to_csv(
        LOG_FILE, mode='a', header=False, index=False
    )
    
    return True


# =============================
# FUNGSI UNTUK LOGGING BIN CLOSE DARI ESP32
# =============================
def log_bin_closed(barcode, waste_type, bin_type, duration, weight_status):
    """
    Log bin closed event ke CSV.
    Dipanggil saat ESP32 mengirim konfirmasi bin tertutup.
    """
    timestamp = get_timestamp()
    
    close_data = {
        "timestamp": timestamp,
        "barcode": barcode,
        "waste_type": waste_type,
        "bin_type": bin_type,
        "bin_state": "closed",
        "bin_duration_sec": duration,
        "weight_status": weight_status
    }
    
    pd.DataFrame([close_data]).to_csv(
        LOG_FILE, mode='a', header=False, index=False
    )
    
    return True


# =============================
# FUNGSI UNTUK UPDATE DURASI (jika ESP32 mengirim durasi aktual)
# =============================
def update_bin_duration(transaction_id, actual_duration):
    """
    Update duration di CSV setelah bin benar-benar tertutup.
    Ini untuk kasus di mana ESP32 mengirim durasi aktual.
    """
    try:
        # Baca file CSV
        df = pd.read_csv(LOG_FILE)
        
        # Cari baris terakhir dengan transaction_id yang sama
        # (perlu menambahkan kolom transaction_id jika diperlukan)
        
        # Untuk sementara, print log
        print(f"📝 Duration update for {transaction_id}: {actual_duration}s")
        
    except Exception as e:
        print(f"❌ Error updating duration: {e}")