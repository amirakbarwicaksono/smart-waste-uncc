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