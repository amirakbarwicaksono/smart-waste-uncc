# # ----------- app/main.py -----------

# import streamlit as st

# st.set_page_config(
#     page_title="Smart Waste System",
#     layout="wide"
# )

# st.title("♻️ Smart Waste Management System")

# st.markdown("""
# ### Welcome 👋

# Use the sidebar to navigate:

# - 👤 **User Mode** → Scan barcode & dispose waste  
# - 🛠️ **Admin Mode** → Test classification & override  
# - 📊 **Dashboard** → Monitor bins in real-time
# - 🎮 **Digital Twin** → Virtual representation of waste bins
# """)

# # Optional: tampilkan preview
# st.divider()
# st.caption("📌 Select a page from the sidebar to get started")

# # ----------- app/main.py -----------
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# import streamlit as st
# import threading
# import time
# from core.mqtt.listener import get_listener, get_messages

# st.set_page_config(
#     page_title="Smart Waste System",
#     layout="wide"
# )

# # =============================
# # INITIALIZE SESSION STATE
# # =============================
# if 'latest_user_id' not in st.session_state:
#     st.session_state.latest_user_id = None

# # =============================
# # START MQTT LISTENER (SEKALI)
# # =============================
# if 'mqtt_started' not in st.session_state:
#     # Start MQTT listener di background
#     listener = get_listener()
#     st.session_state.mqtt_started = True
#     print("✅ MQTT Listener initialized")

# # =============================
# # CHECK FOR NEW MESSAGES (DI MAIN THREAD)
# # =============================
# # Ambil pesan dari queue (ini aman karena di main thread)
# new_messages = get_messages()
# for msg in new_messages:
#     st.session_state.latest_user_id = msg['user_id']
#     print(f"✅ New user from MQTT: {msg['user_id']}")

# # =============================
# # UI MAIN
# # =============================
# st.title("♻️ Smart Waste Management System")

# st.markdown("""
# ### Welcome 👋

# Use the sidebar to navigate:

# - 👤 **User Mode** → Scan & dispose waste  
# - 🛠️ **Admin Mode** → Test classification  
# - 📊 **Dashboard** → Monitor bins in real-time
# - 🎮 **Digital Twin** → Virtual representation
# """)

# # Tampilkan status
# col1, col2 = st.columns(2)
# with col1:
#     st.metric("MQTT Listener", "✅ Active" if st.session_state.mqtt_started else "❌ Inactive")
# with col2:
#     st.metric("Last User ID", st.session_state.latest_user_id or "None")

# st.divider()
# st.caption("📌 Select a page from the sidebar to get started")

# import sys
# import os
# import streamlit as st
# import time

# # Pastikan root directory terdaftar
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from core.mqtt.listener import get_listener, get_messages

# # =============================
# # GLOBAL MQTT SYNC FUNCTION
# # =============================
# def sync_mqtt_to_session():
#     # 1. Pastikan listener running
#     try:
#         get_listener() 
#     except:
#         pass

#     # 2. Ambil pesan
#     new_messages = get_messages()
    
#     if new_messages:
#         # Ambil pesan TERAKHIR saja agar tidak menumpuk
#         last_msg = new_messages[-1] 
        
#         if 'user_id' in last_msg:
#             uid = last_msg['user_id']
#             # Simpan ke session state
#             st.session_state.latest_user_id = uid
#             print(f"🚀 User Detected: {uid}. Redirecting to User Mode...")
            
#             # PINDAH HALAMAN
#             # Catatan: Jika file Anda di folder 'pages', gunakan "pages/user_mode.py"
#             # Jika di root, gunakan "user_mode.py"
#             st.switch_page("pages/user_mode.py") 
#             st.stop() 

# # =============================
# # STREAMLIT CONFIG
# # =============================
# st.set_page_config(page_title="Smart Waste System", layout="wide", page_icon="♻️")

# # Inisialisasi State
# if 'latest_user_id' not in st.session_state:
#     st.session_state.latest_user_id = None

# # CEK MQTT SEBELUM RENDER UI LAINNYA
# sync_mqtt_to_session()

# # =============================
# # MAIN UI
# # =============================
# st.title("♻️ SWMS - UNNC Exchange Students 2026")

# st.markdown("""
# **Ready to dispose of your waste responsibly?**

# Log in to your account, and our system will securely verify your **Hash ID**. Once authenticated, you will be automatically redirected to the Smart Bin interface.
# """)


# # Layout Status
# col1, col2 = st.columns(2)
# with col1:
#     st.metric("System Status", "Online ✅")
# with col2:
#     st.metric("Last User ID", st.session_state.latest_user_id if st.session_state.latest_user_id else "None")

# st.divider()

# # REFRESH LOGIC
# # Hanya rerun jika latest_user_id kosong (sedang menunggu kartu)
# if st.session_state.latest_user_id is None:
#     time.sleep(0.5)
#     st.rerun()

#ini code yang work diatas

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

# st.info("📡 **Waiting for RFID/MQTT signal...**\n\nTap your card or wait for system to detect your user ID.")

# # =============================
# # DEBUG: Tampilkan pesan terakhir
# # =============================
# with st.expander("🔧 Debug - Last MQTT Message"):
#     try:
#         messages = get_messages()
#         if messages:
#             st.write("Raw message:")
#             st.json(messages[-1])
            
#             last = messages[-1]
#             if isinstance(last, dict):
#                 st.write("Keys:", list(last.keys()))
#                 if 'userHashId' in last:
#                     st.success(f"✅ userHashId found: {last['userHashId'][:16]}...")
#                 if 'user_id' in last:
#                     st.info(f"📝 user_id: {last['user_id']}")
#         else:
#             st.write("No messages received yet")
#     except Exception as e:
#         st.write(f"Error: {e}")

# REFRESH LOGIC
if st.session_state.latest_user_id is None:
    time.sleep(0.5)
    st.rerun()