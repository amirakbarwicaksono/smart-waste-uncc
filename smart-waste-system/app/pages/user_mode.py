# # import sys
# # import os
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# # import streamlit as st
# # import pandas as pd

# # from core.barcode.scanner import scan_barcode
# # from core.camera.webcam import capture_image
# # from core.pipeline.processor import process_waste
# # from core.classification.predictor import predict_image

# # LOG_FILE = "logs/transactions.csv"

# # st.header("👤 User Mode")

# # # =============================
# # # SESSION
# # # =============================
# # if "active_user" not in st.session_state:
# #     st.session_state.active_user = None

# # if "session_active" not in st.session_state:
# #     st.session_state.session_active = False

# # # =============================
# # # CHECK-IN
# # # =============================
# # if not st.session_state.session_active:
# #     st.subheader("Step 1: Scan Barcode")

# #     barcode_input = scan_barcode()

# #     if barcode_input:
# #         st.session_state.active_user = barcode_input
# #         st.session_state.session_active = True
# #         st.success(f"✅ Checked In: {barcode_input}")
# #         st.rerun()

# # # =============================
# # # ACTIVE SESSION
# # # =============================
# # if st.session_state.session_active:

# #     st.info(f"👤 Active User: {st.session_state.active_user}")

# #     if st.button("🚪 Check Out"):
# #         st.session_state.active_user = None
# #         st.session_state.session_active = False
# #         st.warning("User Checked Out")
# #         st.rerun()

# #     st.subheader("Step 2: Capture Waste Image")

# #     img = capture_image()

# #     if img is not None:

# #         # UI placeholders
# #         result_box = st.empty()
# #         status_box = st.empty()

# #         # =============================
# #         # STEP 1: PREDICT ONCE
# #         # =============================
# #         waste_type, bin_type = predict_image(img)

# #         result_box.info(f"Waste: {waste_type}")
# #         result_box.success(f"Bin: {bin_type}")

# #         # =============================
# #         # STEP 2: OPENING UI
# #         # =============================
# #         status_box.warning(f"🚪 Opening {bin_type} bin...")

# #         # =============================
# #         # STEP 3: PIPELINE (NO RE-PREDICT)
# #         # =============================
# #         _, _, duration = process_waste(
# #             st.session_state.active_user,
# #             img,
# #             waste_type=waste_type,
# #             bin_type=bin_type
# #         )

# #         # =============================
# #         # STEP 4: CLOSED UI
# #         # =============================
# #         status_box.success(f"✅ Bin closed after {duration:.2f}s")
# # batas coding yang bisa digunakan diatas.

# # # ----------- app/pages/user_mode.py -----------
# # import sys
# # import os
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # from PIL import Image

# # from core.barcode.scanner import scan_barcode
# # from core.camera.webcam import capture_image
# # from core.pipeline.processor import process_waste
# # from core.classification.predictor import predict_image

# # LOG_FILE = "logs/transactions.csv"

# # st.header("👤 User Mode")

# # # =============================
# # # SESSION
# # # =============================
# # if "active_user" not in st.session_state:
# #     st.session_state.active_user = None

# # if "session_active" not in st.session_state:
# #     st.session_state.session_active = False

# # # =============================
# # # CHECK-IN
# # # =============================
# # if not st.session_state.session_active:
# #     st.subheader("Step 1: Scan Barcode")

# #     barcode_input = scan_barcode()

# #     if barcode_input:
# #         st.session_state.active_user = barcode_input
# #         st.session_state.session_active = True
# #         st.success(f"✅ Checked In: {barcode_input}")
# #         st.rerun()

# # # =============================
# # # ACTIVE SESSION
# # # =============================
# # if st.session_state.session_active:

# #     st.info(f"👤 Active User: {st.session_state.active_user}")

# #     if st.button("🚪 Check Out"):
# #         st.session_state.active_user = None
# #         st.session_state.session_active = False
# #         st.warning("User Checked Out")
# #         st.rerun()

# #     st.subheader("Step 2: Capture Waste Image")

# #     img = capture_image()

# #     if img is not None:

# #         # UI placeholders
# #         result_box = st.empty()
# #         status_box = st.empty()

# #         # =============================
# #         # STEP 1: PREDICT ONCE
# #         # =============================
# #         with st.spinner("🔍 Analyzing waste..."):
# #             waste_type, bin_type = predict_image(img)

# #         result_box.info(f"Waste: {waste_type}")
# #         result_box.success(f"Bin: {bin_type}")

# #         # =============================
# #         # STEP 2: OPENING UI
# #         # =============================
# #         status_box.warning(f"🚪 Opening {bin_type} bin...")

# #         # =============================
# #         # STEP 3: PIPELINE (NO RE-PREDICT)
# #         # =============================
# #         _, _, duration = process_waste(
# #             st.session_state.active_user,
# #             img,
# #             waste_type=waste_type,
# #             bin_type=bin_type
# #         )

# #         # =============================
# #         # STEP 4: CLOSED UI
# #         # =============================
# #         status_box.success(f"✅ Bin closed after {duration:.2f}s")
# # #code worrk
# # import sys
# # import os
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# # import streamlit as st
# # import pandas as pd
# # from datetime import datetime, timedelta
# # import json
# # import time
# # from PIL import Image

# # from core.barcode.scanner import scan_barcode
# # from core.camera.webcam import capture_image
# # from core.pipeline.processor import process_waste
# # from core.classification.predictor import predict_image
# # from core.mqtt.client import publish

# # LOG_FILE = "logs/transactions.csv"

# # st.header("👤 User Mode")

# # # =============================
# # # AUTO REFRESH SETUP
# # # =============================
# # if 'refresh_rate' not in st.session_state:
# #     st.session_state.refresh_rate = 1.0  # Refresh setiap 1 detik

# # # =============================
# # # INITIALIZE SESSION STATE
# # # =============================
# # if "active_user" not in st.session_state:
# #     st.session_state.active_user = None

# # if "session_active" not in st.session_state:
# #     st.session_state.session_active = False

# # if "last_activity" not in st.session_state:
# #     st.session_state.last_activity = None

# # if "timeout_seconds" not in st.session_state:
# #     st.session_state.timeout_seconds = 30

# # if "processed_users" not in st.session_state:
# #     st.session_state.processed_users = set()

# # # =============================
# # # CEK USER ID DARI MQTT (MAIN)
# # # =============================
# # latest_user = st.session_state.get('latest_user_id', None)

# # if latest_user and latest_user not in st.session_state.processed_users:
# #     st.session_state.processed_users.add(latest_user)
    
# #     if not st.session_state.session_active:
# #         st.session_state.active_user = latest_user
# #         st.session_state.session_active = True
# #         st.session_state.last_activity = datetime.now()
# #         st.session_state.latest_user_id = None
# #         st.success(f"✅ Auto Check-In via MQTT: {latest_user}")
# #         st.rerun()

# # # =============================
# # # CHECK-IN VIA BARCODE (MANUAL)
# # # =============================
# # if not st.session_state.session_active:
# #     st.subheader("Step 1: Scan Barcode (or wait for MQTT)")
    
# #     # Tampilkan status MQTT
# #     st.caption(f"📡 MQTT Last Received: {latest_user or 'None'}")
    
# #     barcode_input = scan_barcode()

# #     if barcode_input:
# #         st.session_state.active_user = barcode_input
# #         st.session_state.session_active = True
# #         st.session_state.last_activity = datetime.now()
# #         st.success(f"✅ Checked In via Barcode: {barcode_input}")
# #         st.rerun()

# # # =============================
# # # CHECK TIMEOUT (REALTIME)
# # # =============================
# # if st.session_state.session_active and st.session_state.last_activity:
# #     time_since = (datetime.now() - st.session_state.last_activity).total_seconds()
# #     remaining = max(0, st.session_state.timeout_seconds - time_since)
    
# #     # CEK TIMEOUT
# #     if time_since > st.session_state.timeout_seconds:
# #         timeout_payload = {
# #             "timestamp": datetime.now().isoformat(),
# #             "user_id": st.session_state.active_user,
# #             "reason": "inactivity_timeout",
# #             "timeout_seconds": st.session_state.timeout_seconds
# #         }
# #         publish("smartwaste/user/timeout", timeout_payload)
        
# #         st.session_state.active_user = None
# #         st.session_state.session_active = False
# #         st.session_state.last_activity = None
# #         st.warning("⏱️ Auto Check-Out due to inactivity")
# #         st.rerun()

# # # =============================
# # # ACTIVE SESSION
# # # =============================
# # if st.session_state.session_active:
# #     # Hitung ulang remaining untuk ditampilkan
# #     time_since = (datetime.now() - st.session_state.last_activity).total_seconds()
# #     remaining = max(0, st.session_state.timeout_seconds - time_since)
    
# #     # Tampilkan info user dan timer dengan progress bar
# #     col1, col2, col3 = st.columns([2, 1, 1])
# #     with col1:
# #         st.info(f"👤 Active User: {st.session_state.active_user}")
# #     with col2:
# #         # Progress bar untuk visualisasi waktu
# #         progress = 1 - (remaining / st.session_state.timeout_seconds)
# #         st.progress(progress, text=f"⏱️ {int(remaining)}s left")
# #     with col3:
# #         if st.button("🚪 Check Out"):
# #             checkout_payload = {
# #                 "timestamp": datetime.now().isoformat(),
# #                 "user_id": st.session_state.active_user,
# #                 "reason": "manual_checkout"
# #             }
# #             publish("smartwaste/user/timeout", checkout_payload)
            
# #             st.session_state.active_user = None
# #             st.session_state.session_active = False
# #             st.session_state.last_activity = None
# #             st.rerun()

# #     st.subheader("Step 2: Capture or Upload Waste Image")

# #     # Pilihan metode capture
# #     capture_method = st.radio(
# #         "Choose capture method:",
# #         ["📷 Camera", "📁 Upload"],
# #         horizontal=True,
# #         key="capture_method"
# #     )

# #     img = None

# #     if capture_method == "📷 Camera":
# #         # Camera method
# #         if st.button("📸 Take Photo", type="primary", use_container_width=True):
# #             with st.spinner("📸 Capturing image..."):
# #                 img = capture_image()
            
# #             if img is None:
# #                 st.error("❌ Failed to capture image. Please try again or use Upload option.")
# #     else:
# #         # Upload method
# #         uploaded_file = st.file_uploader(
# #             "Choose an image...", 
# #             type=['jpg', 'jpeg', 'png'],
# #             help="Upload a waste image"
# #         )
        
# #         if uploaded_file is not None:
# #             img = Image.open(uploaded_file)
# #             st.image(img, caption="Uploaded Image", use_column_width=True)

# #     # Proses gambar jika ada
# #     if img is not None:
# #         # Update last activity
# #         st.session_state.last_activity = datetime.now()
        
# #         # UI placeholders untuk feedback
# #         result_box = st.empty()
# #         status_box = st.empty()
        
# #         # =============================
# #         # STEP 1: PREDICT
# #         # =============================
# #         with st.spinner("🔍 Analyzing waste type..."):
# #             waste_type, bin_type = predict_image(img)

# #         result_box.info(f"🗑️ Waste: {waste_type}")
# #         result_box.success(f"📦 Bin: {bin_type}")

# #         # =============================
# #         # STEP 2: OPENING UI
# #         # =============================
# #         status_box.warning(f"🚪 Opening {bin_type} bin...")

# #         # =============================
# #         # STEP 3: PIPELINE
# #         # =============================
# #         with st.spinner(f"Processing..."):
# #             _, _, duration = process_waste(
# #                 st.session_state.active_user,
# #                 img,
# #                 waste_type=waste_type,
# #                 bin_type=bin_type
# #             )

# #         # =============================
# #         # STEP 4: CLOSED UI
# #         # =============================
# #         status_box.success(f"✅ Bin closed after {duration:.2f}s")
        
# #         # Update last activity
# #         st.session_state.last_activity = datetime.now()

# # else:
# #     # Tampilan ketika tidak ada session aktif
# #     st.info("⏳ Waiting for user login...")
    
# #     col1, col2 = st.columns(2)
# #     with col1:
# #         st.markdown("""
# #         ### 📡 Auto via MQTT
# #         System will auto-checkin when user ID is received via MQTT.
        
# #         **Topic:** `smartwaste/user/id`
# #         """)
# #     with col2:
# #         st.markdown("""
# #         ### 📱 Manual via Barcode
# #         Use the barcode scanner above to check in manually.
# #         """)
    
# #     st.markdown(f"**MQTT Status:** Last received: `{latest_user or 'None'}`")

# # # =============================
# # # SIDEBAR
# # # =============================
# # st.sidebar.header("⚙️ Settings")

# # # Refresh rate control
# # refresh_rate = st.sidebar.slider(
# #     "Refresh Rate (seconds)",
# #     min_value=0.5,
# #     max_value=5.0,
# #     value=float(st.session_state.refresh_rate),
# #     step=0.5
# # )
# # st.session_state.refresh_rate = refresh_rate

# # st.sidebar.metric("Session", "✅ Active" if st.session_state.session_active else "❌ Waiting")
# # st.sidebar.metric("User", st.session_state.active_user or "None")

# # timeout = st.sidebar.number_input(
# #     "Timeout (s)", 
# #     min_value=5, 
# #     max_value=600, 
# #     value=st.session_state.timeout_seconds,
# #     step=5
# # )
# # if timeout != st.session_state.timeout_seconds:
# #     st.session_state.timeout_seconds = timeout
# #     st.rerun()

# # if st.sidebar.button("🔄 Force Rerun"):
# #     st.rerun()

# # # Debug info
# # with st.sidebar.expander("🔧 Debug Info"):
# #     if st.session_state.session_active:
# #         time_since = (datetime.now() - st.session_state.last_activity).total_seconds()
# #         remaining = max(0, st.session_state.timeout_seconds - time_since)
# #     else:
# #         time_since = 0
# #         remaining = 0
    
# #     debug_data = {
# #         "active_user": st.session_state.active_user,
# #         "session_active": st.session_state.session_active,
# #         "time_since_activity": f"{time_since:.1f}s",
# #         "remaining": f"{remaining:.1f}s",
# #         "processed_users": list(st.session_state.processed_users)[-5:],  # Last 5 users
# #         "latest_mqtt": latest_user,
# #         "refresh_rate": st.session_state.refresh_rate,
# #         "current_time": datetime.now().strftime("%H:%M:%S")
# #     }
# #     st.json(debug_data)
    
# #     # Tombol reset untuk debugging
# #     if st.button("🧹 Reset Processed Users"):
# #         st.session_state.processed_users.clear()
# #         st.rerun()

# # # =============================
# # # AUTO REFRESH LOOP
# # # =============================
# # # Ini akan membuat halaman refresh otomatis setiap N detik
# # time.sleep(st.session_state.refresh_rate)
# # st.rerun()

# # import sys
# # import os
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# # import streamlit as st
# # import pandas as pd
# # from datetime import datetime, timedelta
# # import json
# # import time
# # import cv2
# # from PIL import Image

# # from core.barcode.scanner import scan_barcode
# # from core.camera.webcam import get_camera, capture_image_from_camera
# # from core.pipeline.processor import process_waste
# # from core.classification.predictor import predict_image
# # from core.mqtt.client import publish

# # LOG_FILE = "logs/transactions.csv"

# # st.header("👤 User Mode")

# # # =============================
# # # AUTO REFRESH
# # # =============================
# # if 'refresh_rate' not in st.session_state:
# #     st.session_state.refresh_rate = 1.0

# # # =============================
# # # SESSION STATE
# # # =============================
# # if "active_user" not in st.session_state:
# #     st.session_state.active_user = None

# # if "session_active" not in st.session_state:
# #     st.session_state.session_active = False

# # if "last_activity" not in st.session_state:
# #     st.session_state.last_activity = None

# # if "timeout_seconds" not in st.session_state:
# #     st.session_state.timeout_seconds = 30

# # # Hapus processed_users, kita tidak perlu menyimpan history login
# # if "camera" not in st.session_state:
# #     st.session_state.camera = None

# # # =============================
# # # CEK USER ID DARI MQTT
# # # =============================
# # latest_user = st.session_state.get('latest_user_id', None)

# # # Langsung login tanpa cek processed_users
# # if latest_user and not st.session_state.session_active:
# #     st.session_state.active_user = latest_user
# #     st.session_state.session_active = True
# #     st.session_state.last_activity = datetime.now()
# #     st.session_state.latest_user_id = None  # Reset setelah dipakai
# #     st.success(f"✅ Auto Check-In via MQTT: {latest_user}")
# #     st.rerun()

# # # =============================
# # # BARCODE CHECK-IN
# # # =============================
# # if not st.session_state.session_active:
# #     st.subheader("Step 1: Scan Barcode")
# #     st.caption(f"📡 MQTT Last: {latest_user or 'None'}")
    
# #     barcode_input = scan_barcode()

# #     if barcode_input:
# #         st.session_state.active_user = barcode_input
# #         st.session_state.session_active = True
# #         st.session_state.last_activity = datetime.now()
# #         st.success(f"✅ Checked In: {barcode_input}")
# #         st.rerun()

# # # =============================
# # # TIMEOUT CHECK
# # # =============================
# # if st.session_state.session_active and st.session_state.last_activity:
# #     time_since = (datetime.now() - st.session_state.last_activity).total_seconds()
    
# #     if time_since > st.session_state.timeout_seconds:
# #         publish("smartwaste/user/timeout", {
# #             "timestamp": datetime.now().isoformat(),
# #             "user_id": st.session_state.active_user,
# #             "reason": "inactivity_timeout",
# #             "timeout_seconds": st.session_state.timeout_seconds
# #         })
        
# #         # Reset session
# #         st.session_state.active_user = None
# #         st.session_state.session_active = False
# #         st.session_state.last_activity = None
        
# #         # Reset MQTT user biar bisa login lagi
# #         st.session_state.latest_user_id = None
        
# #         if st.session_state.camera:
# #             st.session_state.camera.release()
# #             st.session_state.camera = None
# #         st.warning("⏱️ Auto Check-Out")
# #         st.rerun()

# # # =============================
# # # ACTIVE SESSION
# # # =============================
# # if st.session_state.session_active:
# #     time_since = (datetime.now() - st.session_state.last_activity).total_seconds()
# #     remaining = max(0, st.session_state.timeout_seconds - time_since)
    
# #     col1, col2, col3 = st.columns([2, 1, 1])
# #     with col1:
# #         st.info(f"👤 User: {st.session_state.active_user}")
# #     with col2:
# #         st.progress(1 - remaining/st.session_state.timeout_seconds, 
# #                    text=f"⏱️ {int(remaining)}s")
# #     with col3:
# #         if st.button("🚪 Check Out"):
# #             publish("smartwaste/user/timeout", {
# #                 "timestamp": datetime.now().isoformat(),
# #                 "user_id": st.session_state.active_user,
# #                 "reason": "manual_checkout"
# #             })
            
# #             # Reset session
# #             st.session_state.active_user = None
# #             st.session_state.session_active = False
# #             st.session_state.last_activity = None
            
# #             # Reset MQTT user biar bisa login lagi
# #             st.session_state.latest_user_id = None
            
# #             if st.session_state.camera:
# #                 st.session_state.camera.release()
# #                 st.session_state.camera = None
# #             st.rerun()

# #     st.subheader("Step 2: Capture Image")

# #     # =============================
# #     # CAMERA PREVIEW
# #     # =============================
# #     if st.session_state.camera is None:
# #         st.session_state.camera = get_camera()
    
# #     if st.session_state.camera:
# #         # Live preview
# #         ret, frame = st.session_state.camera.read()
# #         if ret:
# #             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
# #             st.image(frame_rgb, caption="Live Preview", use_column_width=True)
        
# #         # Capture button
# #         if st.button("📸 Capture & Process", type="primary"):
# #             # Capture image
# #             img = capture_image_from_camera(st.session_state.camera)
            
# #             if img:
# #                 # Update activity
# #                 st.session_state.last_activity = datetime.now()
                
# #                 # UI placeholders
# #                 result = st.empty()
# #                 status = st.empty()
                
# #                 # =============================
# #                 # AI PREDICTION
# #                 # =============================
# #                 with st.spinner("🔍 Analyzing waste type..."):
# #                     waste_type, bin_type = predict_image(img)
                
# #                 # Tampilkan hasil prediksi
# #                 result.info(f"🗑️ **Waste:** {waste_type}")
# #                 result.success(f"📦 **Bin:** {bin_type}")
                
# #                 # =============================
# #                 # OPEN BIN
# #                 # =============================
# #                 status.warning(f"🚪 Opening {bin_type} bin...")
                
# #                 # =============================
# #                 # PROCESS WASTE
# #                 # =============================
# #                 with st.spinner("Processing waste disposal..."):
# #                     _, _, duration = process_waste(
# #                         st.session_state.active_user,
# #                         img,
# #                         waste_type=waste_type,
# #                         bin_type=bin_type
# #                     )
                
# #                 # =============================
# #                 # CLOSED
# #                 # =============================
# #                 status.success(f"✅ Bin closed after {duration:.2f}s")
# #                 st.session_state.last_activity = datetime.now()
# #             else:
# #                 st.error("❌ Failed to capture")
# #     else:
# #         st.error("❌ Camera not available")
# #         if st.button("Retry Camera"):
# #             st.session_state.camera = get_camera()
# #             st.rerun()

# # else:
# #     st.info("⏳ Waiting for user...")
# #     if st.session_state.camera:
# #         st.session_state.camera.release()
# #         st.session_state.camera = None

# # # =============================
# # # SIDEBAR
# # # =============================
# # st.sidebar.header("⚙️ Settings")

# # refresh = st.sidebar.slider("Refresh", 0.5, 5.0, st.session_state.refresh_rate, 0.5)
# # st.session_state.refresh_rate = refresh

# # st.sidebar.metric("Session", "✅" if st.session_state.session_active else "❌")
# # st.sidebar.metric("User", st.session_state.active_user or "None")

# # if st.sidebar.button("🔄 Rerun"):
# #     if st.session_state.camera:
# #         st.session_state.camera.release()
# #         st.session_state.camera = None
# #     st.rerun()

# # # =============================
# # # AUTO REFRESH
# # # =============================
# # time.sleep(st.session_state.refresh_rate)
# # st.rerun()
# # import sys
# # import os
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# # import streamlit as st
# # import pandas as pd
# # from datetime import datetime
# # import time
# # from PIL import Image

# # from core.barcode.scanner import scan_barcode
# # from core.pipeline.processor import process_waste
# # from core.classification.predictor import predict_image
# # from core.mqtt.client import publish

# # st.set_page_config(page_title="Smart Waste User Mode", page_icon="👤")

# # from core.mqtt.listener import get_listener, get_messages

# # # Panggil fungsi sinkronisasi di paling atas agar selalu update
# # def sync_mqtt_in_user_mode():
# #     new_messages = get_messages()
# #     for msg in new_messages:
# #         if 'user_id' in msg:
# #             # Jika ada ID baru, masukkan ke session state
# #             st.session_state.latest_user_id = msg['user_id']
# #             # Opsional: Berikan feedback di console
# #             print(f"📥 New MQTT Login detected in User Mode: {msg['user_id']}")

# # # Jalankan pengecekan pesan MQTT
# # sync_mqtt_in_user_mode()

# # # =============================
# # # INITIALIZE SESSION STATE
# # # =============================
# # if "state" not in st.session_state:
# #     st.session_state.state = {
# #         "active_user": None,
# #         "session_active": False,
# #         "last_activity": None,
# #         "timeout_seconds": 30,
# #         "last_result": None,
# #         "processed": False,
# #         "refresh_rate": 2.0,
# #         "uploader_key": 0  # Used to reset camera/upload widgets
# #     }

# # def reset_session():
# #     st.session_state.state.update({
# #         "active_user": None,
# #         "session_active": False,
# #         "last_activity": None,
# #         "last_result": None,
# #         "processed": False,
# #         "uploader_key": st.session_state.state["uploader_key"] + 1
# #     })
# #     st.session_state.latest_user_id = None

# # # =============================
# # # MQTT & AUTO CHECK-IN
# # # =============================
# # latest_user = st.session_state.get('latest_user_id', None)
# # if latest_user and not st.session_state.state["session_active"]:
# #     st.session_state.state["active_user"] = latest_user
# #     st.session_state.state["session_active"] = True
# #     st.session_state.state["last_activity"] = datetime.now()
# #     st.session_state.latest_user_id = None
# #     st.rerun()

# # # =============================
# # # HEADER & SIDEBAR
# # # =============================
# # st.header("👤 User Mode")

# # with st.sidebar:
# #     st.header("⚙️ Settings")
# #     st.session_state.state["refresh_rate"] = st.slider("Refresh Rate (s)", 0.5, 5.0, 2.0)
# #     st.metric("Status", "✅ Active" if st.session_state.state["session_active"] else "❌ Waiting")
    
# #     if st.button("🔄 Force Clear/Reset"):
# #         reset_session()
# #         st.rerun()

# # # =============================
# # # LOGIC: NOT LOGGED IN
# # # =============================
# # if not st.session_state.state["session_active"]:
# #     st.subheader("Step 1: Scan Barcode or Wait for Card")
# #     barcode_input = scan_barcode()
# #     if barcode_input:
# #         st.session_state.state["active_user"] = barcode_input
# #         st.session_state.state["session_active"] = True
# #         st.session_state.state["last_activity"] = datetime.now()
# #         st.rerun()
# #     st.info("⏳ Waiting for barcode scan or MQTT signal...")
# #     st.stop()

# # # =============================
# # # LOGIC: ACTIVE SESSION
# # # =============================
# # elapsed = (datetime.now() - st.session_state.state["last_activity"]).total_seconds()
# # remaining = max(0, st.session_state.state["timeout_seconds"] - elapsed)

# # if remaining <= 0:
# #     publish("smartwaste/user/timeout", {"user_id": st.session_state.state["active_user"], "reason": "timeout"})
# #     reset_session()
# #     st.warning("⏱️ Session Ended (Timeout)")
# #     st.rerun()

# # # Info bar
# # col_user, col_timer, col_out = st.columns([2, 2, 1])
# # col_user.info(f"👤 **User:** {st.session_state.state['active_user']}")
# # col_timer.progress(remaining / st.session_state.state["timeout_seconds"], text=f"⏱️ {int(remaining)}s")
# # if col_out.button("🚪 Logout"):
# #     reset_session()
# #     st.rerun()

# # st.divider()

# # # =============================
# # # STEP 2: CLASSIFICATION
# # # =============================
# # st.subheader("Step 2: Waste Identification")

# # # Display form only if not yet processed
# # if not st.session_state.state["processed"]:
# #     method = st.radio("Method:", ["📷 Camera", "📁 Upload"], horizontal=True)
# #     img_file = None

# #     # Using uploader_key to reset widgets when "Dispose More" is clicked
# #     if method == "📷 Camera":
# #         img_file = st.camera_input("Take a photo of the waste", key=f"cam_{st.session_state.state['uploader_key']}")
# #     else:
# #         img_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'], key=f"file_{st.session_state.state['uploader_key']}")

# #     if img_file:
# #         img = Image.open(img_file)
# #         st.session_state.state["last_activity"] = datetime.now()
        
# #         with st.status("🛠️ Processing Waste...", expanded=True) as status:
# #             st.write("🔍 Analyzing image (AI)...")
# #             waste_type, bin_type = predict_image(img)
            
# #             st.write(f"📦 Opening {bin_type} bin...")
# #             _, _, duration = process_waste(
# #                 st.session_state.state["active_user"], 
# #                 img, 
# #                 waste_type=waste_type, 
# #                 bin_type=bin_type
# #             )
            
# #             st.session_state.state["last_result"] = {
# #                 "waste": waste_type,
# #                 "bin": bin_type,
# #                 "duration": duration
# #             }
# #             st.session_state.state["processed"] = True
# #             status.update(label="✅ Completed!", state="complete")
        
# #         st.rerun()
# # else:
# #     # Display last result if already processed
# #     if st.session_state.state["last_result"]:
# #         res = st.session_state.state["last_result"]
# #         st.success(f"### Success!\nType: **{res['waste']}** \nBin: **{res['bin']}** \nDuration: **{res['duration']:.1f}s**")
        
# #         if st.button("♻️ Dispose More Waste", type="primary"):
# #             # RESET KEYS: Increment uploader_key, set processed to False
# #             st.session_state.state["processed"] = False
# #             st.session_state.state["last_result"] = None
# #             st.session_state.state["uploader_key"] += 1 
# #             st.session_state.state["last_activity"] = datetime.now() # Reset activity timer
# #             st.rerun()

# # # =============================
# # # SMART REFRESH
# # # =============================
# # # Only auto-rerun if waiting for input (not yet processed)
# # if not st.session_state.state["processed"]:
# #     time.sleep(st.session_state.state["refresh_rate"])
# #     st.rerun()
# # import sys
# # import os
# # sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# # import streamlit as st
# # import pandas as pd
# # from datetime import datetime
# # import time
# # from PIL import Image

# # from core.barcode.scanner import scan_barcode
# # from core.pipeline.processor import process_waste
# # from core.classification.predictor import predict_image
# # from core.mqtt.client import publish
# # from core.mqtt.listener import get_listener, get_messages

# # st.set_page_config(page_title="Smart Waste User Mode", page_icon="👤")

# # # Panggil fungsi sinkronisasi di paling atas agar selalu update
# # def sync_mqtt_in_user_mode():
# #     get_listener() # Pastikan listener running
# #     new_messages = get_messages()
# #     for msg in new_messages:
# #         if 'user_id' in msg:
# #             st.session_state.latest_user_id = msg['user_id']
# #             print(f"📥 New MQTT Login detected in User Mode: {msg['user_id']}")

# # sync_mqtt_in_user_mode()

# # # =============================
# # # INITIALIZE SESSION STATE
# # # =============================
# # if "state" not in st.session_state:
# #     st.session_state.state = {
# #         "active_user": None,
# #         "session_active": False,
# #         "last_activity": None,
# #         "timeout_seconds": 30,
# #         "last_result": None,
# #         "processed": False,
# #         "refresh_rate": 2.0,
# #         "uploader_key": 0 
# #     }

# # def reset_session():
# #     st.session_state.state.update({
# #         "active_user": None,
# #         "session_active": False,
# #         "last_activity": None,
# #         "last_result": None,
# #         "processed": False,
# #         "uploader_key": st.session_state.state["uploader_key"] + 1
# #     })
# #     st.session_state.latest_user_id = None

# # # =============================
# # # MQTT & AUTO CHECK-IN
# # # =============================
# # latest_user = st.session_state.get('latest_user_id', None)
# # if latest_user and not st.session_state.state["session_active"]:
# #     st.session_state.state["active_user"] = latest_user
# #     st.session_state.state["session_active"] = True
# #     st.session_state.state["last_activity"] = datetime.now()
# #     st.session_state.latest_user_id = None
# #     st.rerun()

# # # =============================
# # # HEADER & SIDEBAR
# # # =============================
# # st.header("👤 User Mode")

# # with st.sidebar:
# #     st.header("⚙️ Settings")
# #     st.session_state.state["refresh_rate"] = st.slider("Refresh Rate (s)", 0.5, 5.0, 2.0)
# #     st.metric("Status", "✅ Active" if st.session_state.state["session_active"] else "❌ Waiting")
    
# #     if st.button("🔄 Force Clear/Reset"):
# #         reset_session()
# #         st.switch_page("main.py") # <--- Balik ke main saat reset paksa

# # # =============================
# # # LOGIC: NOT LOGGED IN
# # # =============================
# # if not st.session_state.state["session_active"]:
# #     st.subheader("Step 1: Scan Barcode or Wait for Card")
# #     barcode_input = scan_barcode()
# #     if barcode_input:
# #         st.session_state.state["active_user"] = barcode_input
# #         st.session_state.state["session_active"] = True
# #         st.session_state.state["last_activity"] = datetime.now()
# #         st.rerun()
# #     st.info("⏳ Waiting for barcode scan or MQTT signal...")
    
# #     # Gunakan rerun alih-alih stop agar MQTT tetap terpantau di halaman ini
# #     time.sleep(st.session_state.state["refresh_rate"])
# #     st.rerun()

# # # =============================
# # # LOGIC: ACTIVE SESSION
# # # =============================
# # elapsed = (datetime.now() - st.session_state.state["last_activity"]).total_seconds()
# # remaining = max(0, st.session_state.state["timeout_seconds"] - elapsed)

# # # --- UPDATE LOGIKA TIMEOUT ---
# # if remaining <= 0:
# #     publish("smartwaste/user/timeout", {"user_id": st.session_state.state["active_user"], "reason": "timeout"})
# #     reset_session()
# #     st.session_state.latest_user_id = None #Tambahan
# #     st.warning("⏱️ Session Ended (Timeout). Redirecting...")
# #     time.sleep(2) # Beri waktu user membaca pesan
# #     st.switch_page("main.py") # <--- REDIRECT KE MAIN

# # # Info bar
# # col_user, col_timer, col_out = st.columns([2, 2, 1])
# # col_user.info(f"👤 **User:** {st.session_state.state['active_user']}")
# # col_timer.progress(remaining / st.session_state.state["timeout_seconds"], text=f"⏱️ {int(remaining)}s")

# # if col_out.button("🚪 Logout"):
# #     reset_session()
# #     # Inside reset_session() in user_mode.py
# #     st.session_state.latest_user_id = None
# #     st.switch_page("main.py") # <--- REDIRECT KE MAIN SAAT LOGOUT

# # st.divider()

# # # =============================
# # # STEP 2: CLASSIFICATION
# # # =============================
# # st.subheader("Step 2: Waste Identification")

# # if not st.session_state.state["processed"]:
# #     method = st.radio("Method:", ["📷 Camera", "📁 Upload"], horizontal=True)
# #     img_file = None

# #     if method == "📷 Camera":
# #         img_file = st.camera_input("Take a photo of the waste", key=f"cam_{st.session_state.state['uploader_key']}")
# #     else:
# #         img_file = st.file_uploader("Choose an image file", type=['jpg', 'jpeg', 'png'], key=f"file_{st.session_state.state['uploader_key']}")

# #     if img_file:
# #         img = Image.open(img_file)
# #         st.session_state.state["last_activity"] = datetime.now()
        
# #         with st.status("🛠️ Processing Waste...", expanded=True) as status:
# #             st.write("🔍 Analyzing image (AI)...")
# #             waste_type, bin_type = predict_image(img)
            
# #             st.write(f"📦 Opening {bin_type} bin...")
# #             _, _, duration = process_waste(
# #                 st.session_state.state["active_user"], 
# #                 img, 
# #                 waste_type=waste_type, 
# #                 bin_type=bin_type
# #             )
            
# #             st.session_state.state["last_result"] = {
# #                 "waste": waste_type,
# #                 "bin": bin_type,
# #                 "duration": duration
# #             }
# #             st.session_state.state["processed"] = True
# #             status.update(label="✅ Completed!", state="complete")
        
# #         st.rerun()
# # else:
# #     if st.session_state.state["last_result"]:
# #         res = st.session_state.state["last_result"]
# #         st.success(f"### Success!\nType: **{res['waste']}** \nBin: **{res['bin']}** \nDuration: **{res['duration']:.1f}s**")
        
# #         if st.button("♻️ Dispose More Waste", type="primary"):
# #             st.session_state.state["processed"] = False
# #             st.session_state.state["last_result"] = None
# #             st.session_state.state["uploader_key"] += 1 
# #             st.session_state.state["last_activity"] = datetime.now()
# #             st.rerun()

# # # =============================
# # # SMART REFRESH
# # # =============================
# # if not st.session_state.state["processed"]:
# #     time.sleep(st.session_state.state["refresh_rate"])
# #     st.rerun()

# import sys
# import os
# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import time
# from PIL import Image

# # Setup Path agar bisa import core module
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# from core.barcode.scanner import scan_barcode
# from core.pipeline.processor import process_waste
# from core.classification.predictor import predict_image
# from core.mqtt.client import publish
# from core.mqtt.listener import get_listener, get_messages

# # =============================
# # STREAMLIT CONFIG
# # =============================
# st.set_page_config(
#     page_title="Smart Waste User Mode", 
#     page_icon="👤", 
#     layout="wide"
# )

# # =============================
# # INITIALIZE SESSION STATE
# # =============================
# if "state" not in st.session_state:
#     st.session_state.state = {
#         "active_user": None,
#         "session_active": False,
#         "last_activity": None,
#         "timeout_seconds": 0,
#         "last_result": None,
#         "processed": False,
#         "refresh_rate": 2.0, 
#         "uploader_key": 0
#     }

# if 'latest_user_id' not in st.session_state:
#     st.session_state.latest_user_id = None

# def reset_session():
#     st.session_state.state.update({
#         "active_user": None,
#         "session_active": False,
#         "last_activity": None,
#         "last_result": None,
#         "processed": False,
#         "uploader_key": st.session_state.state["uploader_key"] + 1
#     })
#     st.session_state.latest_user_id = None

# # =============================
# # MQTT SYNC LOGIC
# # =============================
# def sync_mqtt_in_user_mode():
#     """Memeriksa pesan MQTT baru untuk auto-login."""
#     get_listener() 
#     new_messages = get_messages()
#     for msg in new_messages:
#         if 'user_id' in msg:
#             st.session_state.latest_user_id = msg['user_id']
#             print(f"📥 New MQTT Login detected: {msg['user_id']}")

# sync_mqtt_in_user_mode()

# # AUTO LOGIN LOGIC
# if st.session_state.latest_user_id and not st.session_state.state["session_active"]:
#     st.session_state.state["active_user"] = st.session_state.latest_user_id
#     st.session_state.state["session_active"] = True
#     st.session_state.state["last_activity"] = datetime.now()
#     st.session_state.latest_user_id = None 
#     st.rerun()

# # =============================
# # HEADER & SIDEBAR
# # =============================
# st.header("👤 User Mode")

# with st.sidebar:
#     st.header("⚙️ Settings")
#     st.session_state.state["refresh_rate"] = st.slider("Auto Refresh (s)", 0.5, 5.0, 2.0)
#     st.metric("Status", "✅ Active" if st.session_state.state["session_active"] else "❌ Waiting")
    
#     if st.button("🔄 Exit to Main"):
#         reset_session()
#         st.switch_page("main.py")

# # =============================
# # MAIN LOGIC FLOW
# # =============================

# # KONDISI A: BELUM LOGIN
# if not st.session_state.state["session_active"]:
#     st.subheader("Step 1: Scan Barcode or Wait for Card")
    
#     col_scan, col_info = st.columns([1, 1])
#     with col_scan:
#         barcode_input = scan_barcode()
#         if barcode_input:
#             st.session_state.state["active_user"] = barcode_input
#             st.session_state.state["session_active"] = True
#             st.session_state.state["last_activity"] = datetime.now()
#             st.rerun()
            
#     with col_info:
#         st.info("⏳ **Waiting...**\n\nScan your barcode or tap your card to begin.")
    
#     # Refresh otomatis agar MQTT tetap terpantau saat logout
#     time.sleep(st.session_state.state["refresh_rate"])
#     st.rerun()

# # KONDISI B: SESI AKTIF
# else:
#     # 1. Check Timeout
#     elapsed = (datetime.now() - st.session_state.state["last_activity"]).total_seconds()
#     remaining = max(0, st.session_state.state["timeout_seconds"] - elapsed)

#     if remaining <= 0:
#         publish("smartwaste/user/timeout", {"user_id": st.session_state.state["active_user"], "reason": "timeout"})
#         reset_session()
#         st.warning("⏱️ Session Ended (Timeout). Redirecting...")
#         time.sleep(2)
#         st.switch_page("main.py")

#     # 2. User Info & Timer
#     col_user, col_timer, col_out = st.columns([2, 2, 1])
#     col_user.info(f"👤 **User:** {st.session_state.state['active_user']}")
#     col_timer.progress(remaining / st.session_state.state["timeout_seconds"], text=f"⏱️ {int(remaining)}s remaining")
    
#     if col_out.button("🚪 Logout", use_container_width=True):
#         reset_session()
#         st.switch_page("main.py")

#     st.divider()

#     # 3. Waste Identification
#     st.subheader("Step 2: Waste Identification")
    
#     img_file = None # Inisialisasi awal

#     if not st.session_state.state["processed"]:
#         method = st.radio("Method:", ["📷 Camera", "📁 Upload"], horizontal=True)

#         if method == "📷 Camera":
#             img_file = st.camera_input("Take a photo", key=f"cam_{st.session_state.state['uploader_key']}")
#         else:
#             img_file = st.file_uploader("Upload image", type=['jpg', 'jpeg', 'png'], key=f"file_{st.session_state.state['uploader_key']}")

#         # PROSES JIKA FILE MASUK
#         if img_file is not None:
#             # Update activity agar tidak timeout saat AI bekerja
#             st.session_state.state["last_activity"] = datetime.now()
            
#             with st.status("🛠️ Processing Waste...", expanded=True) as status:
#                 img = Image.open(img_file)
#                 st.write("🔍 Analyzing image (AI)...")
#                 waste_type, bin_type = predict_image(img)
                
#                 st.write(f"📦 Opening {bin_type} bin...")
#                 _, _, duration = process_waste(
#                     st.session_state.state["active_user"], 
#                     img, 
#                     waste_type=waste_type, 
#                     bin_type=bin_type
#                 )
                
#                 st.session_state.state["last_result"] = {
#                     "waste": waste_type,
#                     "bin": bin_type,
#                     "duration": duration
#                 }
#                 st.session_state.state["processed"] = True
#                 status.update(label="✅ Success!", state="complete")
            
#             # Rerun sekali untuk menampilkan hasil sukses
#             st.rerun()

#     else:
#         # TAMPILKAN HASIL
#         if st.session_state.state["last_result"]:
#             res = st.session_state.state["last_result"]
#             st.success(f"### Success!\nType: **{res['waste']}** | Bin: **{res['bin']}** | Time: **{res['duration']:.1f}s**")
            
#             if st.button("♻️ Dispose More Waste", type="primary"):
#                 st.session_state.state["processed"] = False
#                 st.session_state.state["last_result"] = None
#                 st.session_state.state["uploader_key"] += 1 
#                 st.session_state.state["last_activity"] = datetime.now()
#                 st.rerun()

#     # =============================
#     # SMART REFRESH LOGIC
#     # =============================
#     # Jangan refresh jika: sudah diproses ATAU sedang ada file di uploader
#     if not st.session_state.state["processed"] and img_file is None:
#         time.sleep(1.0) # Refresh timer setiap detik
#         st.rerun()

import sys
import os
import streamlit as st
import pandas as pd
from datetime import datetime
import time
from PIL import Image

# Setup Path agar bisa import core module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from core.barcode.scanner import scan_barcode
from core.pipeline.processor import process_waste
from core.classification.predictor import predict_image
from core.mqtt.client import publish
from core.mqtt.listener import get_listener, get_messages

# =============================
# STREAMLIT CONFIG
# =============================
st.set_page_config(
    page_title="Smart Waste User Mode", 
    page_icon="👤", 
    layout="wide"
)

# =============================
# INITIALIZE SESSION STATE
# =============================
if "state" not in st.session_state:
    st.session_state.state = {
        "active_user": None,
        "session_active": False,
        "last_activity": None,
        "timeout_seconds": 100,
        "last_result": None,
        "processed": False,
        "refresh_rate": 2.0, 
        "uploader_key": 0
    }

if 'latest_user_id' not in st.session_state:
    st.session_state.latest_user_id = None

def reset_session():
    st.session_state.state.update({
        "active_user": None,
        "session_active": False,
        "last_activity": None,
        "last_result": None,
        "processed": False,
        "uploader_key": st.session_state.state["uploader_key"] + 1
    })
    st.session_state.latest_user_id = None

# =============================
# MQTT SYNC LOGIC
# =============================
def sync_mqtt_in_user_mode():
    """Memeriksa pesan MQTT baru untuk auto-login."""
    get_listener() 
    new_messages = get_messages()
    for msg in new_messages:
        if 'user_id' in msg:
            st.session_state.latest_user_id = msg['user_id']
            print(f"📥 New MQTT Login detected: {msg['user_id']}")

sync_mqtt_in_user_mode()

# AUTO LOGIN LOGIC
if st.session_state.latest_user_id and not st.session_state.state["session_active"]:
    st.session_state.state["active_user"] = st.session_state.latest_user_id
    st.session_state.state["session_active"] = True
    st.session_state.state["last_activity"] = datetime.now()
    st.session_state.latest_user_id = None 
    st.rerun()

# =============================
# HEADER & SIDEBAR
# =============================
st.header("👤 User Mode")

with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.state["refresh_rate"] = st.slider("Auto Refresh (s)", 0.5, 5.0, 2.0)
    st.metric("Status", "✅ Active" if st.session_state.state["session_active"] else "❌ Waiting")
    
    if st.button("🔄 Exit to Main"):
        reset_session()
        st.switch_page("main.py")

# =============================
# MAIN LOGIC FLOW
# =============================

# KONDISI A: BELUM LOGIN
if not st.session_state.state["session_active"]:
    st.subheader("Step 1: Scan Barcode or Wait for Card")
    
    col_scan, col_info = st.columns([1, 1])
    with col_scan:
        barcode_input = scan_barcode()
        if barcode_input:
            st.session_state.state["active_user"] = barcode_input
            st.session_state.state["session_active"] = True
            st.session_state.state["last_activity"] = datetime.now()
            st.rerun()
            
    with col_info:
        st.info("⏳ **Waiting...**\n\nScan your barcode or tap your card to begin.")
    
    # Refresh otomatis agar MQTT tetap terpantau saat logout
    time.sleep(st.session_state.state["refresh_rate"])
    st.rerun()

# KONDISI B: SESI AKTIF
else:
    # 1. Check Timeout
    elapsed = (datetime.now() - st.session_state.state["last_activity"]).total_seconds()
    remaining = max(0, st.session_state.state["timeout_seconds"] - elapsed)

    if remaining <= 0:
        publish("smartwaste/user/timeout", {"user_id": st.session_state.state["active_user"], "reason": "timeout"})
        reset_session()
        st.warning("⏱️ Session Ended (Timeout). Redirecting...")
        time.sleep(2)
        st.switch_page("main.py")

    # 2. User Info & Timer
    col_user, col_timer, col_out = st.columns([2, 2, 1])
    col_user.info(f"👤 **User:** {st.session_state.state['active_user']}")
    col_timer.progress(remaining / st.session_state.state["timeout_seconds"], text=f"⏱️ {int(remaining)}s remaining")
    
    if col_out.button("🚪 Logout", use_container_width=True):
        reset_session()
        st.switch_page("main.py")

    st.divider()

    # 3. Waste Identification
    st.subheader("Step 2: Waste Identification")
    
    img_file = None # Inisialisasi awal

    if not st.session_state.state["processed"]:
        method = st.radio("Method:", ["📷 Camera", "📁 Upload"], horizontal=True)

        if method == "📷 Camera":
            img_file = st.camera_input("Take a photo", key=f"cam_{st.session_state.state['uploader_key']}")
        else:
            img_file = st.file_uploader("Upload image", type=['jpg', 'jpeg', 'png'], key=f"file_{st.session_state.state['uploader_key']}")

        # PROSES JIKA FILE MASUK
        if img_file is not None:
            # Update activity agar tidak timeout saat AI bekerja
            st.session_state.state["last_activity"] = datetime.now()
            
            with st.status("🛠️ Processing Waste...", expanded=True) as status:
                img = Image.open(img_file)
                st.write("🔍 Analyzing image (AI)...")
                waste_type, bin_type = predict_image(img)
                
                st.write(f"📦 Opening {bin_type} bin...")
                _, _, duration = process_waste(
                    st.session_state.state["active_user"], 
                    img, 
                    waste_type=waste_type, 
                    bin_type=bin_type
                )
                
                st.session_state.state["last_result"] = {
                    "waste": waste_type,
                    "bin": bin_type,
                    "duration": duration
                }
                st.session_state.state["processed"] = True
                status.update(label="✅ Success!", state="complete")
            
            # Rerun sekali untuk menampilkan hasil sukses
            st.rerun()

    else:
        # TAMPILKAN HASIL
        if st.session_state.state["last_result"]:
            res = st.session_state.state["last_result"]
            st.success(f"### Success!\nType: **{res['waste']}** | Bin: **{res['bin']}** | Time: **{res['duration']:.1f}s**")
            
            if st.button("♻️ Dispose More Waste", type="primary"):
                st.session_state.state["processed"] = False
                st.session_state.state["last_result"] = None
                st.session_state.state["uploader_key"] += 1 
                st.session_state.state["last_activity"] = datetime.now()
                st.rerun()

    # =============================
    # SMART REFRESH LOGIC
    # =============================
    # Jangan refresh jika: sudah diproses ATAU sedang ada file di uploader
    if not st.session_state.state["processed"] and img_file is None:
        time.sleep(0.5) # Refresh timer setiap detik
        st.rerun()
