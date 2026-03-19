
# # ----------- core/camera/webcam.py -----------
# import streamlit as st

# def capture_image():
#     return st.camera_input("Capture Waste Image")

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

# # ----------- core/camera/webcam.py -----------
# import cv2
# import numpy as np
# from PIL import Image
# import time
# import platform
# import streamlit as st

# def capture_image():
#     """
#     Capture image from webcam with better error handling
#     Returns: PIL Image or None if failed
#     """
#     try:
#         # Deteksi OS
#         system = platform.system()
        
#         # Coba beberapa camera index
#         camera_indices = [0, 1]
#         cap = None
        
#         for idx in camera_indices:
#             try:
#                 # Untuk macOS, gunakan backend AVFOUNDATION
#                 if system == "Darwin":  # macOS
#                     cap = cv2.VideoCapture(idx, cv2.CAP_AVFOUNDATION)
#                 else:
#                     cap = cv2.VideoCapture(idx)
                
#                 if cap.isOpened():
#                     # Test baca frame
#                     ret, frame = cap.read()
#                     if ret and frame is not None:
#                         print(f"✅ Camera opened with index {idx}")
#                         break
#                     else:
#                         cap.release()
#                         cap = None
#             except Exception as e:
#                 print(f"⚠️ Error with camera index {idx}: {e}")
#                 if cap:
#                     cap.release()
#                 cap = None
        
#         if cap is None or not cap.isOpened():
#             print("❌ No camera found")
#             return None
        
#         # Beri waktu camera untuk stabil
#         time.sleep(0.5)
        
#         # Capture beberapa frame untuk memastikan camera ready
#         for _ in range(3):
#             ret, frame = cap.read()
#             time.sleep(0.1)
        
#         # Capture final frame
#         ret, frame = cap.read()
        
#         # Tutup camera
#         cap.release()
        
#         if ret and frame is not None:
#             # Convert BGR to RGB
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
#             # Convert to PIL Image
#             img = Image.fromarray(frame_rgb)
            
#             print(f"✅ Image captured: {img.size}")
#             return img
#         else:
#             print("❌ Failed to capture frame")
#             return None
            
#     except Exception as e:
#         print(f"❌ Camera error: {e}")
#         return None
# # # ----------- core/camera/webcam.py -----------
# # import cv2
# # import numpy as np
# # from PIL import Image
# # import time
# # import platform
# # import streamlit as st

# # def get_camera():
# #     """Get camera instance without capturing"""
# #     try:
# #         system = platform.system()
# #         camera_indices = [0, 1]
        
# #         for idx in camera_indices:
# #             try:
# #                 if system == "Darwin":
# #                     cap = cv2.VideoCapture(idx, cv2.CAP_AVFOUNDATION)
# #                 else:
# #                     cap = cv2.VideoCapture(idx)
                
# #                 if cap.isOpened():
# #                     ret, frame = cap.read()
# #                     if ret and frame is not None:
# #                         print(f"✅ Camera opened with index {idx}")
# #                         return cap
# #                     else:
# #                         cap.release()
# #             except:
# #                 pass
# #         return None
# #     except Exception as e:
# #         print(f"❌ Camera error: {e}")
# #         return None

# # def capture_image_from_camera(cap):
# #     """Capture image from camera instance"""
# #     try:
# #         # Capture frame
# #         ret, frame = cap.read()
        
# #         if ret and frame is not None:
# #             # Convert BGR to RGB
# #             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
# #             # Convert to PIL Image
# #             img = Image.fromarray(frame_rgb)
            
# #             print(f"✅ Image captured: {img.size}")
# #             return img
# #         else:
# #             print("❌ Failed to capture frame")
# #             return None
# #     except Exception as e:
# #         print(f"❌ Capture error: {e}")
# #         return None

# # def capture_image():
# #     """Legacy function for backward compatibility"""
# #     cap = get_camera()
# #     if cap:
# #         img = capture_image_from_camera(cap)
# #         cap.release()
# #         return img
# #     return None

# ----------- core/camera/webcam.py -----------
import cv2
import numpy as np
from PIL import Image
import time
import platform

def get_camera():
    """
    Get camera instance without capturing
    Returns: cv2.VideoCapture object or None if failed
    """
    try:
        system = platform.system()
        camera_indices = [0, 1]
        
        for idx in camera_indices:
            try:
                if system == "Darwin":  # macOS
                    cap = cv2.VideoCapture(idx, cv2.CAP_AVFOUNDATION)
                else:
                    cap = cv2.VideoCapture(idx)
                
                if cap.isOpened():
                    # Test baca frame
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        print(f"✅ Camera opened with index {idx}")
                        return cap
                    else:
                        cap.release()
            except Exception as e:
                print(f"⚠️ Error with camera index {idx}: {e}")
                if cap:
                    cap.release()
        
        print("❌ No camera found")
        return None
        
    except Exception as e:
        print(f"❌ Camera error: {e}")
        return None

def capture_image_from_camera(cap):
    """
    Capture image from camera instance
    Args:
        cap: cv2.VideoCapture object (from get_camera())
    Returns: PIL Image or None if failed
    """
    try:
        if cap is None or not cap.isOpened():
            print("❌ Camera not opened")
            return None
        
        # Capture frame
        ret, frame = cap.read()
        
        if ret and frame is not None:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL Image
            img = Image.fromarray(frame_rgb)
            
            print(f"✅ Image captured: {img.size}")
            return img
        else:
            print("❌ Failed to capture frame")
            return None
            
    except Exception as e:
        print(f"❌ Capture error: {e}")
        return None

def capture_image():
    """
    Legacy function for backward compatibility
    Returns: PIL Image or None if failed
    """
    cap = get_camera()
    if cap:
        img = capture_image_from_camera(cap)
        cap.release()
        return img
    return None