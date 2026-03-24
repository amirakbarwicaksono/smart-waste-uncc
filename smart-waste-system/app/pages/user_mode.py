# import sys
# import os
# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import time
# from PIL import Image

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# from core.barcode.scanner import scan_barcode
# from core.pipeline.processor import process_waste
# from core.classification.predictor import predict_image
# from core.mqtt.client import publish
# from core.mqtt.listener import get_listener, get_messages

# st.set_page_config(page_title="Smart Waste User Mode", page_icon="👤", layout="wide")

# # =============================
# # INITIALIZE SESSION STATE
# # =============================
# if "state" not in st.session_state:
#     st.session_state.state = {
#         "active_user_id": None,
#         "active_user_hash": None,
#         "session_active": False,
#         "last_activity": None,
#         "timeout_seconds": 100,
#         "last_result": None,
#         "processed": False,
#         "refresh_rate": 2.0, 
#         "uploader_key": 0,
#         "predicted_waste": None,
#         "predicted_bin": None,
#         "predicted_img": None,
#         "weight_status": None,
#         "weight_confirmed": False,
#         "processing": False
#     }

# if 'latest_user_id' not in st.session_state:
#     st.session_state.latest_user_id = None
# if 'latest_user_hash' not in st.session_state:
#     st.session_state.latest_user_hash = None
# if 'latest_user_name' not in st.session_state:
#     st.session_state.latest_user_name = None

# def reset_session():
#     st.session_state.state.update({
#         "active_user_id": None,
#         "active_user_hash": None,
#         "session_active": False,
#         "last_activity": None,
#         "last_result": None,
#         "processed": False,
#         "uploader_key": st.session_state.state["uploader_key"] + 1,
#         "predicted_waste": None,
#         "predicted_bin": None,
#         "predicted_img": None,
#         "weight_status": None,
#         "weight_confirmed": False,
#         "processing": False
#     })
#     st.session_state.latest_user_id = None
#     st.session_state.latest_user_hash = None
#     st.session_state.latest_user_name = None

# # =============================
# # MQTT SYNC
# # =============================
# def sync_mqtt_in_user_mode():
#     get_listener() 
#     new_messages = get_messages()
#     for msg in new_messages:
#         if isinstance(msg, dict):
#             if 'userHashId' in msg:
#                 st.session_state.latest_user_hash = msg['userHashId']
#                 st.session_state.latest_user_name = msg.get('user_id', None)
#             elif 'user_id' in msg:
#                 st.session_state.latest_user_id = msg['user_id']

# sync_mqtt_in_user_mode()

# # =============================
# # AUTO LOGIN
# # =============================
# if st.session_state.latest_user_hash and not st.session_state.state["session_active"]:
#     st.session_state.state["active_user_hash"] = st.session_state.latest_user_hash
#     st.session_state.state["active_user_id"] = st.session_state.latest_user_name
#     st.session_state.state["session_active"] = True
#     st.session_state.state["last_activity"] = datetime.now()
#     st.session_state.latest_user_hash = None
#     st.session_state.latest_user_name = None
#     st.success(f"✅ Auto Check-In: {st.session_state.state['active_user_id'] or 'User'}")
#     st.rerun()

# elif st.session_state.latest_user_id and not st.session_state.state["session_active"]:
#     st.session_state.state["active_user_id"] = st.session_state.latest_user_id
#     st.session_state.state["active_user_hash"] = None
#     st.session_state.state["session_active"] = True
#     st.session_state.state["last_activity"] = datetime.now()
#     st.session_state.latest_user_id = None
#     st.success(f"✅ Manual Check-In: {st.session_state.state['active_user_id']}")
#     st.rerun()

# # =============================
# # HEADER & SIDEBAR
# # =============================
# st.header("👤 User Mode")

# with st.sidebar:
#     st.header("⚙️ Settings")
#     st.session_state.state["refresh_rate"] = st.slider("Auto Refresh (s)", 0.5, 5.0, 2.0)
#     st.metric("Status", "✅ Active" if st.session_state.state["session_active"] else "❌ Waiting")
#     if st.session_state.state["session_active"]:
#         st.metric("User", st.session_state.state["active_user_id"] or "Unknown")
#     # HAPUS tombol Exit to Main di sidebar (tidak perlu, sudah ada Logout di main area)
#     # if st.button("🔄 Exit to Main"):
#     #     reset_session()
#     #     st.switch_page("main.py")

# # =============================
# # MAIN LOGIC
# # =============================
# if not st.session_state.state["session_active"]:
#     st.subheader("Step 1: Scan Barcode or Wait for Card")
#     col_scan, col_info = st.columns([1, 1])
#     with col_scan:
#         barcode_input = scan_barcode()
#         if barcode_input:
#             st.session_state.state["active_user_id"] = barcode_input
#             st.session_state.state["session_active"] = True
#             st.session_state.state["last_activity"] = datetime.now()
#             st.success(f"✅ Checked In: {barcode_input}")
#             st.rerun()
#     with col_info:
#         st.info("⏳ **Waiting...**\n\nScan your barcode or tap your card.")
#     time.sleep(st.session_state.state["refresh_rate"])
#     st.rerun()

# else:
#     elapsed = (datetime.now() - st.session_state.state["last_activity"]).total_seconds()
#     remaining = max(0, st.session_state.state["timeout_seconds"] - elapsed)

#     if remaining <= 0:
#         publish("smartwaste/user/timeout", {"user_id": st.session_state.state["active_user_id"], "reason": "timeout"})
#         reset_session()
#         st.warning("⏱️ Session Timeout")
#         time.sleep(2)
#         st.switch_page("main.py")

#     # User info row (tanpa tombol Logout di sini)
#     col_user, col_timer = st.columns([3, 1])
#     col_user.info(f"👤 **User:** {st.session_state.state['active_user_id']}")
#     col_timer.progress(remaining / st.session_state.state["timeout_seconds"], text=f"⏱️ {int(remaining)}s left")

#     st.divider()
    
#     # =============================
#     # STEP 2: AI PREDICT
#     # =============================
#     st.subheader("Step 2: Identify Waste")
    
#     if not st.session_state.state["predicted_waste"]:
#         method = st.radio("Method:", ["📷 Camera", "📁 Upload"], horizontal=True)
#         img_file = None
#         if method == "📷 Camera":
#             img_file = st.camera_input("Take a photo", key=f"cam_{st.session_state.state['uploader_key']}")
#         else:
#             img_file = st.file_uploader("Upload image", type=['jpg', 'jpeg', 'png'], key=f"file_{st.session_state.state['uploader_key']}")
        
#         if img_file:
#             with st.spinner("🔍 AI analyzing..."):
#                 img = Image.open(img_file)
#                 waste_type, bin_type = predict_image(img)
#                 st.session_state.state["predicted_waste"] = waste_type
#                 st.session_state.state["predicted_bin"] = bin_type
#                 st.session_state.state["predicted_img"] = img
#                 st.session_state.state["last_activity"] = datetime.now()
#                 st.success(f"✅ {waste_type} → {bin_type}")
#                 st.rerun()
    
#     else:
#         waste_type = st.session_state.state["predicted_waste"]
#         bin_type = st.session_state.state["predicted_bin"]
        
#         st.info(f"🗑️ **Waste:** {waste_type}")
#         st.success(f"📦 **Bin:** {bin_type}")
#         st.divider()
        
#         # =============================
#         # STEP 3: WEIGHT CONFIRMATION
#         # =============================
#         st.subheader("Step 3: Confirm Disposal")
#         st.markdown("**Did sensor actually detect weight?**")
        
#         if not st.session_state.state["weight_confirmed"]:
#             col_yes, col_no = st.columns(2)
#             with col_yes:
#                 if st.button("✅ Sensor Detected Weight", type="primary"):
#                     st.session_state.state["weight_status"] = True
#                     st.session_state.state["weight_confirmed"] = True
#                     st.session_state.state["last_activity"] = datetime.now()
#                     st.success("✅ Confirmed!")
#                     st.rerun()
            
#             with col_no:
#                 if st.button("❌ Sensor Did Not Detect Weight", type="secondary"):
#                     st.session_state.state["weight_status"] = False
#                     st.session_state.state["weight_confirmed"] = True
#                     st.session_state.state["last_activity"] = datetime.now()
#                     st.warning("⚠️ Noted.")
#                     st.rerun()
        
#         else:
#             # Tampilkan status yang sudah dipilih
#             if st.session_state.state["weight_status"]:
#                 st.success("✅ Status: True")
#             else:
#                 st.warning("⚠️ Status: False")
            
#             # AUTO OPEN BIN SETELAH WEIGHT CONFIRMED
#             if not st.session_state.state["processed"] and not st.session_state.state["processing"]:
#                 st.session_state.state["processing"] = True
                
#                 with st.status("Opening bin...", expanded=True) as status:
#                     user_identifier = st.session_state.state["active_user_hash"] or st.session_state.state["active_user_id"]
#                     img = st.session_state.state["predicted_img"]
#                     weight_status = st.session_state.state["weight_status"]
                    
#                     # Process waste - weight_status akan disimpan di CSV oleh processor
#                     _, _, duration = process_waste(
#                         user_identifier, img, 
#                         waste_type=waste_type, bin_type=bin_type,
#                         weight_status=weight_status
#                     )
                    
#                     st.session_state.state["last_result"] = {
#                         "waste": waste_type, "bin": bin_type, 
#                         "duration": duration
#                     }
#                     st.session_state.state["processed"] = True
#                     status.update(label="✅ Bin closed!", state="complete")
                
#                 st.rerun()
        
#         # =============================
#         # TAMPILKAN HASIL SETELAH PROSES
#         # =============================
#         if st.session_state.state["processed"] and st.session_state.state["last_result"]:
#             res = st.session_state.state["last_result"]
#             st.success(f"✅ Bin closed after {res['duration']:.1f}s")
            
#             col1, col2 = st.columns(2)
            
#             with col1:
#                 if st.button("♻️ Dispose More Waste", type="primary"):
#                     # Publish MQTT untuk disposemore
#                     publish("smartwaste/user/dispose", {
#                         "user_id": st.session_state.state["active_user_id"],
#                         "reason": "disposemore"
#                     })
                    
#                     # Reset session untuk proses berikutnya
#                     st.session_state.state["predicted_waste"] = None
#                     st.session_state.state["predicted_bin"] = None
#                     st.session_state.state["predicted_img"] = None
#                     st.session_state.state["processed"] = False
#                     st.session_state.state["weight_status"] = None
#                     st.session_state.state["weight_confirmed"] = False
#                     st.session_state.state["processing"] = False
#                     st.session_state.state["uploader_key"] += 1
#                     st.rerun()
            
#             with col2:
#                 if st.button("🚪 Logout", type="secondary"):
#                     publish("smartwaste/user/timeout", {
#                         "user_id": st.session_state.state["active_user_id"],
#                         "reason": "logout"
#                     })
#                     reset_session()
#                     st.switch_page("main.py")

#     if not st.session_state.state["processed"] and not st.session_state.state["predicted_waste"]:
#         time.sleep(0.5)
#         st.rerun()

#last code work for Weight Confirmation.

import sys
import os
import streamlit as st
import pandas as pd
from datetime import datetime
import time
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.barcode.scanner import scan_barcode
from core.pipeline.processor import process_waste
from core.classification.predictor import predict_image
from core.mqtt.client import publish
from core.mqtt.listener import get_listener, get_messages

st.set_page_config(page_title="Smart Waste User Mode", page_icon="👤", layout="wide")

# =============================
# INITIALIZE SESSION STATE
# =============================
if "state" not in st.session_state:
    st.session_state.state = {
        "active_user_id": None,
        "active_user_hash": None,
        "session_active": False,
        "last_activity": None,
        "timeout_seconds": 100,
        "last_result": None,
        "processed": False,
        "refresh_rate": 2.0, 
        "uploader_key": 0,
        "predicted_waste": None,
        "predicted_bin": None,
        "predicted_img": None,
        "weight_status": None,
        "weight_confirmed": False,
        "processing": False
    }

if 'latest_user_id' not in st.session_state:
    st.session_state.latest_user_id = None
if 'latest_user_hash' not in st.session_state:
    st.session_state.latest_user_hash = None
if 'latest_user_name' not in st.session_state:
    st.session_state.latest_user_name = None

def reset_session():
    st.session_state.state.update({
        "active_user_id": None,
        "active_user_hash": None,
        "session_active": False,
        "last_activity": None,
        "last_result": None,
        "processed": False,
        "uploader_key": st.session_state.state["uploader_key"] + 1,
        "predicted_waste": None,
        "predicted_bin": None,
        "predicted_img": None,
        "weight_status": None,
        "weight_confirmed": False,
        "processing": False
    })
    st.session_state.latest_user_id = None
    st.session_state.latest_user_hash = None
    st.session_state.latest_user_name = None

# =============================
# MQTT SYNC
# =============================
def sync_mqtt_in_user_mode():
    get_listener() 
    new_messages = get_messages()
    for msg in new_messages:
        if isinstance(msg, dict):
            if 'userHashId' in msg:
                st.session_state.latest_user_hash = msg['userHashId']
                st.session_state.latest_user_name = msg.get('user_id', None)
            elif 'user_id' in msg:
                st.session_state.latest_user_id = msg['user_id']

sync_mqtt_in_user_mode()

# =============================
# AUTO LOGIN
# =============================
if st.session_state.latest_user_hash and not st.session_state.state["session_active"]:
    st.session_state.state["active_user_hash"] = st.session_state.latest_user_hash
    st.session_state.state["active_user_id"] = st.session_state.latest_user_name
    st.session_state.state["session_active"] = True
    st.session_state.state["last_activity"] = datetime.now()
    st.session_state.latest_user_hash = None
    st.session_state.latest_user_name = None
    st.success(f"✅ Auto Check-In: {st.session_state.state['active_user_id'] or 'User'}")
    st.rerun()

elif st.session_state.latest_user_id and not st.session_state.state["session_active"]:
    st.session_state.state["active_user_id"] = st.session_state.latest_user_id
    st.session_state.state["active_user_hash"] = None
    st.session_state.state["session_active"] = True
    st.session_state.state["last_activity"] = datetime.now()
    st.session_state.latest_user_id = None
    st.success(f"✅ Manual Check-In: {st.session_state.state['active_user_id']}")
    st.rerun()

# =============================
# HEADER & SIDEBAR
# =============================
st.header("👤 User Mode")

with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.state["refresh_rate"] = st.slider("Auto Refresh (s)", 0.5, 5.0, 2.0)
    st.metric("Status", "✅ Active" if st.session_state.state["session_active"] else "❌ Waiting")
    if st.session_state.state["session_active"]:
        st.metric("User", st.session_state.state["active_user_id"] or "Unknown")
    # HAPUS tombol Exit to Main di sidebar (tidak perlu, sudah ada Logout di main area)
    # if st.button("🔄 Exit to Main"):
    #     reset_session()
    #     st.switch_page("main.py")

# =============================
# MAIN LOGIC
# =============================
if not st.session_state.state["session_active"]:
    st.subheader("Step 1: Scan Barcode or Wait for Card")
    col_scan, col_info = st.columns([1, 1])
    with col_scan:
        barcode_input = scan_barcode()
        if barcode_input:
            st.session_state.state["active_user_id"] = barcode_input
            st.session_state.state["session_active"] = True
            st.session_state.state["last_activity"] = datetime.now()
            st.success(f"✅ Checked In: {barcode_input}")
            st.rerun()
    with col_info:
        st.info("⏳ **Waiting...**\n\nScan your barcode or tap your card.")
    time.sleep(st.session_state.state["refresh_rate"])
    st.rerun()

else:
    elapsed = (datetime.now() - st.session_state.state["last_activity"]).total_seconds()
    remaining = max(0, st.session_state.state["timeout_seconds"] - elapsed)

    if remaining <= 0:
        publish("smartwaste/user/timeout", {"user_id": st.session_state.state["active_user_id"], "reason": "timeout"})
        reset_session()
        st.warning("⏱️ Session Timeout")
        time.sleep(2)
        st.switch_page("main.py")

    # User info row (tanpa tombol Logout di sini)
    col_user, col_timer = st.columns([3, 1])
    col_user.info(f"👤 **User:** {st.session_state.state['active_user_id']}")
    col_timer.progress(remaining / st.session_state.state["timeout_seconds"], text=f"⏱️ {int(remaining)}s left")

    st.divider()
    
    # =============================
    # STEP 2: AI PREDICT
    # =============================
    st.subheader("Step 2: Identify Waste")
    
    if not st.session_state.state["predicted_waste"]:
        method = st.radio("Method:", ["📷 Camera", "📁 Upload"], horizontal=True)
        img_file = None
        if method == "📷 Camera":
            img_file = st.camera_input("Take a photo", key=f"cam_{st.session_state.state['uploader_key']}")
        else:
            img_file = st.file_uploader("Upload image", type=['jpg', 'jpeg', 'png'], key=f"file_{st.session_state.state['uploader_key']}")
        
        if img_file:
            with st.spinner("🔍 AI analyzing..."):
                img = Image.open(img_file)
                waste_type, bin_type = predict_image(img)
                st.session_state.state["predicted_waste"] = waste_type
                st.session_state.state["predicted_bin"] = bin_type
                st.session_state.state["predicted_img"] = img
                st.session_state.state["last_activity"] = datetime.now()
                st.success(f"✅ {waste_type} → {bin_type}")
                st.rerun()
    
    else:
        waste_type = st.session_state.state["predicted_waste"]
        bin_type = st.session_state.state["predicted_bin"]
        
        st.info(f"🗑️ **Waste:** {waste_type}")
        st.success(f"📦 **Bin:** {bin_type}")
        st.divider()
        
        # =============================
        # STEP 3: WEIGHT CONFIRMATION
        # =============================
        st.subheader("Step 3: Confirm Disposal")
        st.markdown("**Did sensor actually detect weight?**")
        
        if not st.session_state.state["weight_confirmed"]:
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("✅ Sensor Detected Weight", type="primary"):
                    st.session_state.state["weight_status"] = True
                    st.session_state.state["weight_confirmed"] = True
                    st.session_state.state["last_activity"] = datetime.now()
                    st.success("✅ Confirmed!")
                    st.rerun()
            
            with col_no:
                if st.button("❌ Sensor Did Not Detect Weight", type="secondary"):
                    st.session_state.state["weight_status"] = False
                    st.session_state.state["weight_confirmed"] = True
                    st.session_state.state["last_activity"] = datetime.now()
                    st.warning("⚠️ Noted.")
                    st.rerun()
        
        else:
            # Tampilkan status yang sudah dipilih
            if st.session_state.state["weight_status"]:
                st.success("✅ Status: True")
            else:
                st.warning("⚠️ Status: False")
            
            # AUTO OPEN BIN SETELAH WEIGHT CONFIRMED
            if not st.session_state.state["processed"] and not st.session_state.state["processing"]:
                st.session_state.state["processing"] = True
                
                with st.status("Opening bin...", expanded=True) as status:
                    user_identifier = st.session_state.state["active_user_hash"] or st.session_state.state["active_user_id"]
                    img = st.session_state.state["predicted_img"]
                    weight_status = st.session_state.state["weight_status"]
                    
                    # Process waste - weight_status akan disimpan di CSV oleh processor
                    _, _, duration = process_waste(
                        user_identifier, img, 
                        waste_type=waste_type, bin_type=bin_type,
                        weight_status=weight_status
                    )
                    
                    st.session_state.state["last_result"] = {
                        "waste": waste_type, "bin": bin_type, 
                        "duration": duration
                    }
                    st.session_state.state["processed"] = True
                    status.update(label="✅ Bin closed!", state="complete")
                
                st.rerun()
        
        # =============================
        # TAMPILKAN HASIL SETELAH PROSES
        # =============================
        if st.session_state.state["processed"] and st.session_state.state["last_result"]:
            res = st.session_state.state["last_result"]
            st.success(f"✅ Bin closed after {res['duration']:.1f}s")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("♻️ Dispose More Waste", type="primary"):
                    # Publish MQTT untuk disposemore
                    publish("smartwaste/user/dispose", {
                        "user_id": st.session_state.state["active_user_id"],
                        "reason": "disposemore"
                    })
                    
                    # Reset session untuk proses berikutnya
                    st.session_state.state["predicted_waste"] = None
                    st.session_state.state["predicted_bin"] = None
                    st.session_state.state["predicted_img"] = None
                    st.session_state.state["processed"] = False
                    st.session_state.state["weight_status"] = None
                    st.session_state.state["weight_confirmed"] = False
                    st.session_state.state["processing"] = False
                    st.session_state.state["uploader_key"] += 1
                    st.rerun()
            
            with col2:
                if st.button("🚪 Logout", type="secondary"):
                    publish("smartwaste/user/timeout", {
                        "user_id": st.session_state.state["active_user_id"],
                        "reason": "logout"
                    })
                    reset_session()
                    st.switch_page("main.py")

    if not st.session_state.state["processed"] and not st.session_state.state["predicted_waste"]:
        time.sleep(0.5)
        st.rerun()