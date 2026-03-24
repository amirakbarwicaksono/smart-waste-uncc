import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from PIL import Image

from core.pipeline.processor import process_waste
from core.classification.predictor import predict_image

st.header("🛠️ Admin Mode")

uploaded_file = st.file_uploader("Upload Waste Image", type=["jpg", "png"])
barcode = st.text_input("Enter Barcode")

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    st.subheader("Override (Optional)")
    waste_override = st.text_input("Waste Type (optional)")
    bin_override = st.selectbox(
        "Select Bin",
        ["recycling", "food_waste", "other", "harmful"]
    )

    if st.button("🚀 Process Waste"):

        if not barcode:
            st.error("Please enter barcode")
            st.stop()

        result_box = st.empty()
        status_box = st.empty()

        # =============================
        # PREDICT FIRST
        # =============================
        waste_type, bin_type = predict_image(img)

        # APPLY OVERRIDE
        final_waste = waste_override if waste_override else waste_type
        final_bin = bin_override if bin_override else bin_type

        result_box.info(f"Waste: {final_waste}")
        result_box.success(f"Bin: {final_bin}")

        status_box.warning(f"🚪 Opening {final_bin} bin...")

        # =============================
        # PIPELINE
        # =============================
        _, _, duration = process_waste(
            barcode=barcode,
            image=img,
            waste_type=final_waste,
            bin_type=final_bin
        )

        status_box.success(f"✅ Closed after {duration:.2f}s")

# # ----------- app/pages/admin_mode.py -----------
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# import streamlit as st
# from PIL import Image
# import io

# from core.pipeline.processor import process_waste
# from core.classification.predictor import predict_image

# st.header("🛠️ Admin Mode")

# uploaded_file = st.file_uploader("Upload Waste Image", type=["jpg", "png", "jpeg"])
# barcode = st.text_input("Enter Barcode")

# if uploaded_file is not None:
#     # Tampilkan gambar
#     img = Image.open(uploaded_file)
#     st.image(img, caption="Uploaded Image", use_container_width=True)
    
#     # Simpan file bytes untuk dikirim ke predictor
#     # Reset file pointer ke awal
#     uploaded_file.seek(0)
    
#     st.subheader("Override (Optional)")
#     waste_override = st.text_input("Waste Type (optional)")
#     bin_override = st.selectbox(
#         "Select Bin",
#         ["recycling", "food_waste", "other", "harmful"]
#     )

#     if st.button("🚀 Process Waste"):

#         if not barcode:
#             st.error("Please enter barcode")
#             st.stop()

#         result_box = st.empty()
#         status_box = st.empty()

#         # =============================
#         # PREDICT FIRST - gunakan uploaded_file langsung
#         # =============================
#         with st.spinner("🔍 Analyzing image..."):
#             # Reset file pointer again before prediction
#             uploaded_file.seek(0)
#             waste_type, bin_type = predict_image(uploaded_file)

#         # APPLY OVERRIDE
#         final_waste = waste_override if waste_override else waste_type
#         final_bin = bin_override if bin_override else bin_type

#         result_box.info(f"Waste: {final_waste}")
#         result_box.success(f"Bin: {final_bin}")

#         status_box.warning(f"🚪 Opening {final_bin} bin...")

#         # =============================
#         # PIPELINE
#         # =============================
#         # Reset file pointer one more time for pipeline
#         uploaded_file.seek(0)
#         _, _, duration = process_waste(
#             barcode=barcode,
#             image=uploaded_file,
#             waste_type=final_waste,
#             bin_type=final_bin
#         )

#         status_box.success(f"✅ Closed after {duration:.2f}s")