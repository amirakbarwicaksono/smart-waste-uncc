import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd

from core.barcode.scanner import scan_barcode
from core.camera.webcam import capture_image
from core.pipeline.processor import process_waste
from core.classification.predictor import predict_image

LOG_FILE = "logs/transactions.csv"

st.header("👤 User Mode")

# =============================
# SESSION
# =============================
if "active_user" not in st.session_state:
    st.session_state.active_user = None

if "session_active" not in st.session_state:
    st.session_state.session_active = False

# =============================
# CHECK-IN
# =============================
if not st.session_state.session_active:
    st.subheader("Step 1: Scan Barcode")

    barcode_input = scan_barcode()

    if barcode_input:
        st.session_state.active_user = barcode_input
        st.session_state.session_active = True
        st.success(f"✅ Checked In: {barcode_input}")
        st.rerun()

# =============================
# ACTIVE SESSION
# =============================
if st.session_state.session_active:

    st.info(f"👤 Active User: {st.session_state.active_user}")

    if st.button("🚪 Check Out"):
        st.session_state.active_user = None
        st.session_state.session_active = False
        st.warning("User Checked Out")
        st.rerun()

    st.subheader("Step 2: Capture Waste Image")

    img = capture_image()

    if img is not None:

        # UI placeholders
        result_box = st.empty()
        status_box = st.empty()

        # =============================
        # STEP 1: PREDICT ONCE
        # =============================
        waste_type, bin_type = predict_image(img)

        result_box.info(f"Waste: {waste_type}")
        result_box.success(f"Bin: {bin_type}")

        # =============================
        # STEP 2: OPENING UI
        # =============================
        status_box.warning(f"🚪 Opening {bin_type} bin...")

        # =============================
        # STEP 3: PIPELINE (NO RE-PREDICT)
        # =============================
        _, _, duration = process_waste(
            st.session_state.active_user,
            img,
            waste_type=waste_type,
            bin_type=bin_type
        )

        # =============================
        # STEP 4: CLOSED UI
        # =============================
        status_box.success(f"✅ Bin closed after {duration:.2f}s")

# # ----------- app/pages/user_mode.py -----------
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# import streamlit as st
# import pandas as pd
# import numpy as np
# from PIL import Image

# from core.barcode.scanner import scan_barcode
# from core.camera.webcam import capture_image
# from core.pipeline.processor import process_waste
# from core.classification.predictor import predict_image

# LOG_FILE = "logs/transactions.csv"

# st.header("👤 User Mode")

# # =============================
# # SESSION
# # =============================
# if "active_user" not in st.session_state:
#     st.session_state.active_user = None

# if "session_active" not in st.session_state:
#     st.session_state.session_active = False

# # =============================
# # CHECK-IN
# # =============================
# if not st.session_state.session_active:
#     st.subheader("Step 1: Scan Barcode")

#     barcode_input = scan_barcode()

#     if barcode_input:
#         st.session_state.active_user = barcode_input
#         st.session_state.session_active = True
#         st.success(f"✅ Checked In: {barcode_input}")
#         st.rerun()

# # =============================
# # ACTIVE SESSION
# # =============================
# if st.session_state.session_active:

#     st.info(f"👤 Active User: {st.session_state.active_user}")

#     if st.button("🚪 Check Out"):
#         st.session_state.active_user = None
#         st.session_state.session_active = False
#         st.warning("User Checked Out")
#         st.rerun()

#     st.subheader("Step 2: Capture Waste Image")

#     img = capture_image()

#     if img is not None:

#         # UI placeholders
#         result_box = st.empty()
#         status_box = st.empty()

#         # =============================
#         # STEP 1: PREDICT ONCE
#         # =============================
#         with st.spinner("🔍 Analyzing waste..."):
#             waste_type, bin_type = predict_image(img)

#         result_box.info(f"Waste: {waste_type}")
#         result_box.success(f"Bin: {bin_type}")

#         # =============================
#         # STEP 2: OPENING UI
#         # =============================
#         status_box.warning(f"🚪 Opening {bin_type} bin...")

#         # =============================
#         # STEP 3: PIPELINE (NO RE-PREDICT)
#         # =============================
#         _, _, duration = process_waste(
#             st.session_state.active_user,
#             img,
#             waste_type=waste_type,
#             bin_type=bin_type
#         )

#         # =============================
#         # STEP 4: CLOSED UI
#         # =============================
#         status_box.success(f"✅ Bin closed after {duration:.2f}s")