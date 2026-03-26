# # Di core/utils/image_saver.py (file baru)
# import os
# import shutil
# from datetime import datetime

# def save_image(image, barcode, waste_type, timestamp):
#     """
#     Menyimpan gambar ke folder logs/images/
#     Mengembalikan path relatif gambar
#     """
#     # Buat folder jika belum ada
#     os.makedirs("logs/images", exist_ok=True)
    
#     # Format nama file: timestamp_barcode_wastetype.jpg
#     filename = f"{timestamp}_{barcode}_{waste_type}.jpg"
#     filepath = f"logs/images/{filename}"
    
#     # Simpan gambar
#     if hasattr(image, 'save'):  # Untuk PIL Image
#         image.save(filepath)
#     else:  # Untuk array numpy (dari kamera)
#         import cv2
#         cv2.imwrite(filepath, image)
    
#     return filepath