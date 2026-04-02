# ----------- core/bin_control/bin_logic.py -----------
"""
Module untuk kontrol bin.
Untuk production dengan ESP32, fungsi ini TIDAK digunakan.
Fungsi ini hanya untuk testing/simulasi tanpa hardware ESP32.
"""

import time
import streamlit as st
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================
# SIMULASI BIN (TANPA ESP32)
# =============================
def open_bin(bin_type):
    """
    SIMULASI hardware bin (tanpa ESP32).
    Fungsi ini HANYA untuk testing/simulasi.
    
    Untuk production dengan ESP32, fungsi ini tidak digunakan.
    ESP32 akan menangani pembukaan bin secara fisik.
    
    Args:
        bin_type: jenis bin (recycling, food_waste, other, harmful)
    
    Returns:
        dict: informasi durasi dan timestamp
    """
    start = time.time()
    logger.info(f"🔧 SIMULATION: Opening {bin_type} bin...")
    
    # Tampilkan status di UI (hanya untuk Streamlit)
    try:
        with st.spinner(f"🚪 Opening {bin_type} bin (simulation)..."):
            time.sleep(30)
    except:
        # Jika tidak dalam konteks Streamlit, hanya sleep
        time.sleep(30)
    
    end = time.time()
    duration = round(end - start, 2)
    
    logger.info(f"✅ SIMULATION: {bin_type} bin closed after {duration}s")
    
    return {
        "bin_type": bin_type,
        "open_timestamp": start,
        "close_timestamp": end,
        "duration": duration,
        "mode": "simulation"
    }


# =============================
# FUNGSI UNTUK ESP32 (REFERENSI)
# =============================
def get_bin_config(bin_type):
    """
    Mengembalikan konfigurasi pin untuk ESP32 berdasarkan jenis bin.
    Fungsi ini untuk referensi saat memprogram ESP32.
    
    Args:
        bin_type: jenis bin (recycling, food_waste, other, harmful)
    
    Returns:
        dict: konfigurasi pin untuk ESP32
    """
    config = {
        "recycling": {
            "bin_type": "recycling",
            "servo_pin": 13,
            "led_red": 14,
            "led_green": 12,
            "led_blue": 27,
            "hx711_dt": 4,
            "hx711_sck": 5,
            "weight_threshold_g": 50
        },
        "food_waste": {
            "bin_type": "food_waste",
            "servo_pin": 13,
            "led_red": 14,
            "led_green": 12,
            "led_blue": 27,
            "hx711_dt": 4,
            "hx711_sck": 5,
            "weight_threshold_g": 50
        },
        "other": {
            "bin_type": "other",
            "servo_pin": 13,
            "led_red": 14,
            "led_green": 12,
            "led_blue": 27,
            "hx711_dt": 4,
            "hx711_sck": 5,
            "weight_threshold_g": 50
        },
        "harmful": {
            "bin_type": "harmful",
            "servo_pin": 13,
            "led_red": 14,
            "led_green": 12,
            "led_blue": 27,
            "hx711_dt": 4,
            "hx711_sck": 5,
            "weight_threshold_g": 50
        }
    }
    
    return config.get(bin_type, config["other"])


def get_mqtt_topics():
    """
    Mengembalikan daftar MQTT topics yang digunakan.
    Untuk referensi saat memprogram ESP32.
    """
    return {
        "bin_control": "smart_waste/bin",      # ESP32 subscribe
        "weight_status": "smartwaste/user/weight",  # ESP32 publish
        "user_login": "smartwaste/user/id",     # ESP32 tidak perlu
        "user_timeout": "smartwaste/user/timeout",  # ESP32 tidak perlu
        "user_dispose": "smartwaste/user/dispose"   # ESP32 tidak perlu
    }


def get_servo_angles():
    """
    Mengembalikan sudut servo untuk buka/tutup.
    Untuk referensi saat memprogram ESP32.
    """
    return {
        "open": 180,    # Sudut untuk membuka bin
        "closed": 0     # Sudut untuk menutup bin
    }


# =============================
# FUNGSI UNTUK TESTING TANPA ESP32
# =============================
def test_bin_sequence(bin_type, weight_detected=True):
    """
    Simulasi urutan bin untuk testing.
    
    Args:
        bin_type: jenis bin
        weight_detected: apakah weight terdeteksi (True/False)
    
    Returns:
        dict: hasil simulasi
    """
    logger.info(f"🧪 TEST: Simulating {bin_type} bin sequence")
    logger.info(f"   Weight detected: {weight_detected}")
    
    start = time.time()
    
    # Simulasi buka bin
    logger.info(f"   📦 Opening bin...")
    time.sleep(1)
    
    # Simulasi deteksi weight
    if weight_detected:
        logger.info(f"   ⚖️ Weight detected! (>{get_bin_config(bin_type)['weight_threshold_g']}g)")
    else:
        logger.info(f"   ⚖️ No weight detected")
    
    # Simulasi bin terbuka
    time.sleep(2)
    
    # Simulasi tutup bin
    logger.info(f"   🔒 Closing bin...")
    time.sleep(1)
    
    duration = round(time.time() - start, 2)
    
    logger.info(f"✅ TEST Complete: {duration}s")
    
    return {
        "bin_type": bin_type,
        "duration": duration,
        "weight_detected": weight_detected,
        "mode": "test"
    }


# =============================
# UTILITY
# =============================
def is_esp32_available():
    """
    Cek apakah ESP32 tersedia (untuk menentukan mode).
    Returns: False (default) - untuk testing tanpa ESP32
    """
    # Di production, fungsi ini bisa dicheck dengan ping ke ESP32
    return False


def get_mode():
    """
    Mengembalikan mode operasi.
    Returns: "simulation" atau "esp32"
    """
    if is_esp32_available():
        return "esp32"
    return "simulation"