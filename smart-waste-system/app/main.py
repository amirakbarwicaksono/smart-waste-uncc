import sys
import os
import streamlit as st
import time
import json

# Pastikan root directory terdaftar
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.mqtt.listener import get_listener, get_messages

# =============================
# GLOBAL MQTT SYNC FUNCTION
# =============================
def sync_mqtt_to_session():
    # 1. Pastikan listener running
    try:
        get_listener() 
    except:
        pass

    # 2. Ambil pesan
    new_messages = get_messages()
    
    if new_messages:
        # Ambil pesan TERAKHIR saja agar tidak menumpuk
        last_msg = new_messages[-1] 
        
        # =============================
        # EKSTRAK DATA DARI PESAN MQTT
        # =============================
        user_id = None
        user_hash = None
        status_transaction = None
        
        # Pesan dari listener sudah berupa dict
        if isinstance(last_msg, dict):
            user_id = last_msg.get('user_id')
            user_hash = last_msg.get('userHashId')
            status_transaction = last_msg.get('statusTransaction')
        
        # PRIORITAS: Gunakan userHashId untuk login (bukan user_id)
        # userHashId adalah identifier utama
        if user_hash:
            # Simpan ke session state - GUNAKAN HASH ID SEBAGAI IDENTIFIER UTAMA
            st.session_state.latest_user_id = user_hash  # <-- SIMPAN HASH, BUKAN USER_ID
            st.session_state.latest_user_hash = user_hash
            st.session_state.latest_user_name = user_id  # Simpan user_id sebagai nama
            st.session_state.latest_status = status_transaction
            
            print(f"🚀 User Detected by Hash: {user_hash[:16]}...")
            print(f"   User Name: {user_id}")
            if status_transaction:
                print(f"   Status: {status_transaction}")
            
            # PINDAH HALAMAN
            st.switch_page("pages/user_mode.py") 
            st.stop()
        elif user_id:
            # Fallback: jika tidak ada hash, gunakan user_id (untuk kompatibilitas)
            st.session_state.latest_user_id = user_id
            st.session_state.latest_user_hash = None
            st.session_state.latest_user_name = user_id
            print(f"⚠️ No hash found, using user_id: {user_id}")
            st.switch_page("pages/user_mode.py")
            st.stop()
        else:
            print(f"⚠️ No valid identifier in message: {last_msg}")

# =============================
# STREAMLIT CONFIG
# =============================
st.set_page_config(page_title="Smart Waste System", layout="wide", page_icon="♻️")

# Inisialisasi State
if 'latest_user_id' not in st.session_state:
    st.session_state.latest_user_id = None
    
if 'latest_user_hash' not in st.session_state:
    st.session_state.latest_user_hash = None
    
if 'latest_user_name' not in st.session_state:
    st.session_state.latest_user_name = None
    
if 'latest_status' not in st.session_state:
    st.session_state.latest_status = None

# CEK MQTT SEBELUM RENDER UI LAINNYA
sync_mqtt_to_session()

# =============================
# MAIN UI
# =============================
st.title("♻️ SWMS - UNNC Exchange Students 2026")

st.markdown("""
**Ready to dispose of your waste responsibly?**

Log in to your account, and our system will securely verify your **Hash ID**. Once authenticated, you will be automatically redirected to the Smart Bin interface.
""")

# Layout Status
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("System Status", "Online ✅")
with col2:
    last_id = st.session_state.latest_user_id if st.session_state.latest_user_id else "None"
    if last_id != "None" and len(last_id) > 16:
        last_id = last_id[:16] + "..."
    st.metric("User Hash", last_id)
with col3:
    last_name = st.session_state.latest_user_name if st.session_state.latest_user_name else "None"
    st.metric("User Name", last_name)
with col4:
    last_status = st.session_state.latest_status if st.session_state.latest_status else "None"
    st.metric("Status", last_status)

st.divider()

# REFRESH LOGIC
if st.session_state.latest_user_id is None:
    time.sleep(0.5)
    st.rerun()