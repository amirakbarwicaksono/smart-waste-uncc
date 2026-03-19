
# ----------- core/camera/webcam.py -----------
import streamlit as st

def capture_image():
    return st.camera_input("Capture Waste Image")

# import streamlit as st

# def capture_image():
#     st.subheader("📷 Capture or Upload Waste Image")

#     tab1, tab2 = st.tabs(["📷 Camera", "📁 Upload"])

#     img = None

#     # =============================
#     # CAMERA TAB
#     # =============================
#     with tab1:
#         st.caption("Use camera (recommended on phone)")

#         img = st.camera_input("Take a photo")

#         if img is None:
#             st.info("👉 If camera doesn't work, use Upload tab")

#     # =============================
#     # UPLOAD TAB (FALLBACK)
#     # =============================
#     with tab2:
#         uploaded = st.file_uploader(
#             "Upload image",
#             type=["jpg", "jpeg", "png"]
#         )

#         if uploaded is not None:
#             img = uploaded

#     return img