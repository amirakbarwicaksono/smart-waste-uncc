# # ----------- core/classification/predictor.py -----------
# import numpy as np
# from PIL import Image
# import tensorflow as tf
# import os
# import json
# import random

# from core.classification.labels import WASTE_CLASSES, BIN_MAPPING
# from core.classification.model import load_trained_model

# # Paths
# MODEL_PATH = "models/waste_classifier.h5"
# CLASS_INDICES_PATH = "models/class_indices.json"

# # Load model once at import
# model = None
# class_indices = None

# def load_model():
#     """Load model and class indices"""
#     global model, class_indices
    
#     # Load class indices
#     if os.path.exists(CLASS_INDICES_PATH):
#         with open(CLASS_INDICES_PATH, 'r') as f:
#             class_indices = json.load(f)
#         # Reverse mapping: index -> class name
#         class_indices = {v: k for k, v in class_indices.items()}
#     else:
#         # Default mapping
#         class_indices = {i: WASTE_CLASSES[i] for i in range(len(WASTE_CLASSES))}
    
#     # Load model
#     model = load_trained_model(MODEL_PATH)
#     if model:
#         print("✅ Model loaded successfully")
#     else:
#         print("⚠️ No model found. Using random prediction as fallback.")

# # Load model at import
# load_model()

# def preprocess_image(img, target_size=(224, 224)):
#     """
#     Preprocess image for model input
#     """
#     if isinstance(img, str):
#         # If img is file path
#         img = Image.open(img)
    
#     # Convert to RGB if needed
#     if img.mode != 'RGB':
#         img = img.convert('RGB')
    
#     # Resize image
#     img = img.resize(target_size)
    
#     # Convert to array and normalize
#     img_array = np.array(img, dtype=np.float32) / 255.0
    
#     # Add batch dimension
#     img_array = np.expand_dims(img_array, axis=0)
    
#     return img_array

# def predict_image(img, return_confidence=False):
#     """
#     Predict waste type from image
#     Returns: (waste_type, bin_type) or (waste_type, bin_type, confidence)
#     """
#     global model, class_indices
    
#     try:
#         # If model exists, use it
#         if model is not None:
#             # Preprocess image
#             processed_img = preprocess_image(img)
            
#             # Make prediction
#             predictions = model.predict(processed_img, verbose=0)[0]
            
#             # Get predicted class
#             predicted_idx = np.argmax(predictions)
#             confidence = float(predictions[predicted_idx])
            
#             # Get class name
#             waste = class_indices.get(predicted_idx, WASTE_CLASSES[0])
            
#             # Map to bin type
#             bin_type = BIN_MAPPING.get(waste, "other")
            
#             print(f"✅ AI Prediction: {waste} ({confidence:.2%}) -> {bin_type}")
            
#             if return_confidence:
#                 return waste, bin_type, confidence
#             return waste, bin_type
        
#         else:
#             # Fallback to random
#             return fallback_prediction(return_confidence)
            
#     except Exception as e:
#         print(f"❌ Prediction error: {e}")
#         return fallback_prediction(return_confidence)

# def fallback_prediction(return_confidence=False):
#     """Fallback random prediction when model not available"""
#     waste = random.choice(WASTE_CLASSES)
#     bin_type = BIN_MAPPING.get(waste, "other")
#     confidence = random.uniform(0.5, 0.9)
    
#     print(f"⚠️ Using fallback (random): {waste} -> {bin_type}")
    
#     if return_confidence:
#         return waste, bin_type, confidence
#     return waste, bin_type

# # Test function
# if __name__ == "__main__":
#     print("🧪 Testing predictor...")
    
#     # Test with dummy image
#     test_img = Image.new('RGB', (224, 224), color='red')
    
#     waste, bin_type, conf = predict_image(test_img, return_confidence=True)
#     print(f"\nTest result:")
#     print(f"  Waste: {waste}")
#     print(f"  Bin: {bin_type}")
#     print(f"  Confidence: {conf:.2%}")

# ----------- core/classification/predictor.py -----------
import numpy as np
from PIL import Image
import tensorflow as tf
import os
import json
import random
import io

from core.classification.labels import WASTE_CLASSES, BIN_MAPPING
from core.classification.model import load_trained_model

# Paths
MODEL_PATH = "models/waste_classifier.h5"
CLASS_INDICES_PATH = "models/class_indices.json"

# Load model once at import
model = None
class_indices = None

def load_model():
    """Load model and class indices"""
    global model, class_indices
    
    # Load class indices
    if os.path.exists(CLASS_INDICES_PATH):
        with open(CLASS_INDICES_PATH, 'r') as f:
            class_indices = json.load(f)
        # Reverse mapping: index -> class name
        class_indices = {v: k for k, v in class_indices.items()}
    else:
        # Default mapping
        class_indices = {i: WASTE_CLASSES[i] for i in range(len(WASTE_CLASSES))}
    
    # Load model
    model = load_trained_model(MODEL_PATH)
    if model:
        print("✅ Model loaded successfully")
    else:
        print("⚠️ No model found. Using random prediction as fallback.")

# Load model at import
load_model()

def preprocess_image(img, target_size=(224, 224)):
    """
    Preprocess image for model input
    Supports: PIL Image, file path, numpy array, UploadedFile
    """
    try:
        # CASE 1: Input is already PIL Image
        if isinstance(img, Image.Image):
            pil_image = img
            
        # CASE 2: Input is file path (string)
        elif isinstance(img, str):
            pil_image = Image.open(img)
            
        # CASE 3: Input is numpy array
        elif isinstance(img, np.ndarray):
            pil_image = Image.fromarray(img)
            
        # CASE 4: Input is Streamlit UploadedFile (most important!)
        elif hasattr(img, 'read'):
            # Read the file content
            file_bytes = img.read()
            pil_image = Image.open(io.BytesIO(file_bytes))
            # Reset pointer for future reads (important!)
            img.seek(0)
            
        # CASE 5: Input is bytes
        elif isinstance(img, bytes):
            pil_image = Image.open(io.BytesIO(img))
            
        else:
            print(f"⚠️ Unknown image type: {type(img)}")
            # Return dummy array
            return np.zeros((1, target_size[0], target_size[1], 3), dtype=np.float32)
        
        # Ensure image is in RGB mode
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Resize image
        pil_image = pil_image.resize(target_size, Image.Resampling.LANCZOS)
        
        # Convert to array and normalize
        img_array = np.array(pil_image, dtype=np.float32) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        print(f"✅ Image preprocessed successfully: {img_array.shape}")
        return img_array
        
    except Exception as e:
        print(f"❌ Error preprocessing image: {e}")
        # Return a dummy array as fallback
        return np.zeros((1, target_size[0], target_size[1], 3), dtype=np.float32)

def predict_image(img, return_confidence=False):
    """
    Predict waste type from image
    Returns: (waste_type, bin_type) or (waste_type, bin_type, confidence)
    """
    global model, class_indices
    
    try:
        # If model exists, use it
        if model is not None:
            print(f"🔍 Processing image type: {type(img)}")
            
            # Preprocess image
            processed_img = preprocess_image(img)
            
            # Check if preprocessing returned zeros (error)
            if np.all(processed_img == 0):
                print("⚠️ Preprocessing failed, using fallback")
                return fallback_prediction(return_confidence)
            
            # Make prediction
            predictions = model.predict(processed_img, verbose=0)[0]
            
            # Get predicted class
            predicted_idx = np.argmax(predictions)
            confidence = float(predictions[predicted_idx])
            
            # Get class name
            waste = class_indices.get(predicted_idx, WASTE_CLASSES[0])
            
            # Map to bin type
            bin_type = BIN_MAPPING.get(waste, "other")
            
            print(f"✅ AI Prediction: {waste} ({confidence:.2%}) -> {bin_type}")
            
            if return_confidence:
                return waste, bin_type, confidence
            return waste, bin_type
        
        else:
            # Fallback to random
            return fallback_prediction(return_confidence)
            
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return fallback_prediction(return_confidence)

def fallback_prediction(return_confidence=False):
    """Fallback random prediction when model not available"""
    waste = random.choice(WASTE_CLASSES)
    bin_type = BIN_MAPPING.get(waste, "other")
    confidence = random.uniform(0.5, 0.9)
    
    print(f"⚠️ Using fallback (random): {waste} -> {bin_type}")
    
    if return_confidence:
        return waste, bin_type, confidence
    return waste, bin_type