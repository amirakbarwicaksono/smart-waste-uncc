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

# # ----------- core/classification/predictor.py -----------
# import numpy as np
# from PIL import Image
# import tensorflow as tf
# import os
# import json
# import random
# import io

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
#     Supports: PIL Image, file path, numpy array, UploadedFile
#     """
#     try:
#         # CASE 1: Input is already PIL Image
#         if isinstance(img, Image.Image):
#             pil_image = img
            
#         # CASE 2: Input is file path (string)
#         elif isinstance(img, str):
#             pil_image = Image.open(img)
            
#         # CASE 3: Input is numpy array
#         elif isinstance(img, np.ndarray):
#             pil_image = Image.fromarray(img)
            
#         # CASE 4: Input is Streamlit UploadedFile (most important!)
#         elif hasattr(img, 'read'):
#             # Read the file content
#             file_bytes = img.read()
#             pil_image = Image.open(io.BytesIO(file_bytes))
#             # Reset pointer for future reads (important!)
#             img.seek(0)
            
#         # CASE 5: Input is bytes
#         elif isinstance(img, bytes):
#             pil_image = Image.open(io.BytesIO(img))
            
#         else:
#             print(f"⚠️ Unknown image type: {type(img)}")
#             # Return dummy array
#             return np.zeros((1, target_size[0], target_size[1], 3), dtype=np.float32)
        
#         # Ensure image is in RGB mode
#         if pil_image.mode != 'RGB':
#             pil_image = pil_image.convert('RGB')
        
#         # Resize image
#         pil_image = pil_image.resize(target_size, Image.Resampling.LANCZOS)
        
#         # Convert to array and normalize
#         img_array = np.array(pil_image, dtype=np.float32) / 255.0
        
#         # Add batch dimension
#         img_array = np.expand_dims(img_array, axis=0)
        
#         print(f"✅ Image preprocessed successfully: {img_array.shape}")
#         return img_array
        
#     except Exception as e:
#         print(f"❌ Error preprocessing image: {e}")
#         # Return a dummy array as fallback
#         return np.zeros((1, target_size[0], target_size[1], 3), dtype=np.float32)

# def predict_image(img, return_confidence=False):
#     """
#     Predict waste type from image
#     Returns: (waste_type, bin_type) or (waste_type, bin_type, confidence)
#     """
#     global model, class_indices
    
#     try:
#         # If model exists, use it
#         if model is not None:
#             print(f"🔍 Processing image type: {type(img)}")
            
#             # Preprocess image
#             processed_img = preprocess_image(img)
            
#             # Check if preprocessing returned zeros (error)
#             if np.all(processed_img == 0):
#                 print("⚠️ Preprocessing failed, using fallback")
#                 return fallback_prediction(return_confidence)
            
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
#         import traceback
#         traceback.print_exc()
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


#tryning onix
# # ----------- core/classification/predictor.py -----------
# import numpy as np
# from PIL import Image
# import cv2
# import random
# from pathlib import Path
# import onnxruntime as ort
# import warnings

# warnings.filterwarnings("ignore", message=".*torch.classes.*")

# from core.classification.labels import (
#     CLASS_MAPPING,
#     WASTE_TO_BIN,
#     BIN_TYPES,
#     get_bin_type
# )

# # =============================
# # CONFIGURATION
# # =============================
# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# MODEL_DIR = BASE_DIR / "models"

# INPUT_SIZE = (640, 640)
# CONFIDENCE_THRESHOLD = 0.50

# MODEL_FILES = {
#     "root": MODEL_DIR / "root.onnx",
#     "food": MODEL_DIR / "food.onnx",
#     "other": MODEL_DIR / "other.onnx",
#     "recyclable": MODEL_DIR / "recyclable.onnx",
#     "harmful": MODEL_DIR / "harmful.onnx",
# }

# # ✅ FIXED: Match the training script's REMAP dictionary
# # Root model was trained with these 4 classes:
# # 0: Recyclable (original IDs 0-7)
# # 1: FoodWaste (original IDs 8-10)
# # 2: Others (original IDs 11-21)
# # 3: Harmful (original IDs 22-34)
# ROOT_TO_MODEL = {
#     0: "recyclable",  # ✅ FIXED
#     1: "food",        # ✅ FIXED
#     2: "other",       # ✅ FIXED
#     3: "harmful",     # ✅ Correct
# }

# # =============================
# # LOAD ALL MODELS
# # =============================
# loaded_sessions = {}

# def load_all_models():
#     try:
#         for model_name, model_path in MODEL_FILES.items():
#             if model_path.exists():
#                 session = ort.InferenceSession(str(model_path), providers=['CPUExecutionProvider'])
#                 loaded_sessions[model_name] = session
#                 print(f"✅ Loaded model: {model_name}")
#             else:
#                 print(f"⚠️ Model not found: {model_path}")
#                 loaded_sessions[model_name] = None
#     except Exception as e:
#         print(f"❌ Error loading models: {e}")

# load_all_models()

# # =============================
# # PREPROCESS IMAGE
# # =============================
# def preprocess_image(img, target_size=INPUT_SIZE):
#     try:
#         if isinstance(img, Image.Image):
#             pil_image = img
#         elif isinstance(img, str):
#             pil_image = Image.open(img)
#         elif isinstance(img, np.ndarray):
#             pil_image = Image.fromarray(img)
#         elif hasattr(img, 'read'):
#             import io
#             file_bytes = img.read()
#             pil_image = Image.open(io.BytesIO(file_bytes))
#             img.seek(0)
#         elif isinstance(img, bytes):
#             import io
#             pil_image = Image.open(io.BytesIO(img))
#         else:
#             print(f"⚠️ Unknown image type: {type(img)}")
#             return None
        
#         pil_image = pil_image.resize(target_size, Image.Resampling.LANCZOS)
#         img_array = np.array(pil_image, dtype=np.float32) / 255.0
#         img_array = np.transpose(img_array, (2, 0, 1))
#         img_array = np.expand_dims(img_array, axis=0)
        
#         return img_array
#     except Exception as e:
#         print(f"❌ Error preprocessing image: {e}")
#         return None

# # =============================
# # PARSE YOLOv8 OUTPUT
# # =============================
# def parse_yolo_detection(output, num_classes):
#     try:
#         if output.shape[0] < 5:
#             print(f"⚠️ Invalid output shape: {output.shape}")
#             return None, None
        
#         class_scores = output[4:, :]
#         class_scores = 1 / (1 + np.exp(-class_scores))
#         max_scores_per_class = np.max(class_scores, axis=1)
#         class_id = int(np.argmax(max_scores_per_class))
#         confidence = float(max_scores_per_class[class_id])
        
#         return class_id, confidence
#     except Exception as e:
#         print(f"❌ Error parsing YOLO output: {e}")
#         return None, None

# # =============================
# # RUN INFERENCE
# # =============================
# def run_inference(session, input_data, num_classes):
#     try:
#         input_name = session.get_inputs()[0].name
#         outputs = session.run(None, {input_name: input_data})
#         raw_output = outputs[0][0]
#         class_id, confidence = parse_yolo_detection(raw_output, num_classes)
#         return class_id, confidence
#     except Exception as e:
#         print(f"❌ Inference error: {e}")
#         return None, None

# # =============================
# # HIERARCHICAL PREDICTION
# # =============================
# def predict_image(img, return_confidence=False):
#     try:
#         if "root" not in loaded_sessions or loaded_sessions["root"] is None:
#             print("⚠️ Models not loaded, using fallback")
#             return fallback_prediction(return_confidence)
        
#         processed_img = preprocess_image(img)
#         if processed_img is None:
#             print("⚠️ Preprocessing failed, using fallback")
#             return fallback_prediction(return_confidence)
        
#         # STAGE 1: ROOT CLASSIFICATION
#         print("🔍 Stage 1: Running root classifier...")
        
#         root_class_id, root_confidence = run_inference(
#             loaded_sessions["root"], processed_img, num_classes=4
#         )
        
#         if root_class_id is None:
#             print("⚠️ Root classification failed, using fallback")
#             return fallback_prediction(return_confidence)
        
#         if root_confidence < CONFIDENCE_THRESHOLD:
#             print(f"⚠️ Root confidence too low ({root_confidence:.2%}), using fallback")
#             return fallback_prediction(return_confidence)
        
#         if root_class_id > 3:
#             print(f"⚠️ Invalid root class ID: {root_class_id}, using fallback")
#             return fallback_prediction(return_confidence)
        
#         # ✅ Get category from CORRECTED mapping
#         category_model_name = ROOT_TO_MODEL.get(root_class_id, "other")
#         print(f"📌 Root Category: {category_model_name} ({root_confidence:.2%})")
        
#         # STAGE 2: SPECIFIC CLASSIFICATION
#         print(f"🔍 Stage 2: Running {category_model_name} classifier...")
        
#         if category_model_name not in loaded_sessions or loaded_sessions[category_model_name] is None:
#             print(f"⚠️ Model {category_model_name} not found, using category name")
#             waste_type = category_model_name
#             confidence = root_confidence
#         else:
#             num_specific_classes = len(CLASS_MAPPING.get(category_model_name, {}))
            
#             specific_class_id, specific_confidence = run_inference(
#                 loaded_sessions[category_model_name],
#                 processed_img,
#                 num_classes=num_specific_classes
#             )
            
#             if specific_class_id is not None:
#                 if specific_confidence < CONFIDENCE_THRESHOLD:
#                     print(f"⚠️ Specific confidence low ({specific_confidence:.2%}), using category")
#                     waste_type = category_model_name
#                     confidence = specific_confidence
#                 else:
#                     waste_type = CLASS_MAPPING.get(category_model_name, {}).get(specific_class_id, category_model_name)
#                     confidence = specific_confidence
#                     print(f"📌 Specific Type: {waste_type} ({specific_confidence:.2%})")
#             else:
#                 waste_type = category_model_name
#                 confidence = root_confidence
        
#         bin_type = get_bin_type(waste_type)
#         print(f"✅ Final Prediction: {waste_type} → {bin_type}")
        
#         if return_confidence:
#             return waste_type, bin_type, confidence
#         return waste_type, bin_type
        
#     except Exception as e:
#         print(f"❌ Prediction error: {e}")
#         import traceback
#         traceback.print_exc()
#         return fallback_prediction(return_confidence)

# # =============================
# # FALLBACK
# # =============================
# def fallback_prediction(return_confidence=False):
#     waste = random.choice(list(WASTE_TO_BIN.keys()))
#     bin_type = get_bin_type(waste)
#     confidence = random.uniform(0.5, 0.9)
#     print(f"⚠️ Using fallback (random): {waste} -> {bin_type}")
#     if return_confidence:
#         return waste, bin_type, confidence
#     return waste, bin_type

# import numpy as np
# from PIL import Image
# import cv2
# import random
# from pathlib import Path
# import onnxruntime as ort
# import warnings

# warnings.filterwarnings("ignore", message=".*torch.classes.*")

# from core.classification.labels import (
#     CLASS_MAPPING,
#     WASTE_TO_BIN,
#     BIN_TYPES,
#     get_bin_type
# )

# # =============================
# # CONFIGURATION
# # =============================
# BASE_DIR = Path(__file__).resolve().parent.parent.parent
# MODEL_DIR = BASE_DIR / "models"

# INPUT_SIZE = (640, 640)

# # Per-stage confidence thresholds
# # Stage 1 router — higher threshold, it must be sure before routing
# CONFIDENCE_THRESHOLD_ROOT = 0.30

# # Stage 2 specialists — lower for rare/safety-critical classes
# CONFIDENCE_THRESHOLD_STAGE2 = {
#     "recyclable": 0.25,   # 8 classes, good data volume
#     "food":       0.25,   # 3 classes, reasonable data
#     "other":      0.15,   # 11 classes, many rare sub-classes (Toys=15, Book=15)
#     "harmful":    0.15,   # 13 classes, safety critical — prefer false positives
# }

# MODEL_FILES = {
#     "root":       MODEL_DIR / "root.onnx",
#     "food":       MODEL_DIR / "food.onnx",
#     "other":      MODEL_DIR / "other.onnx",
#     "recyclable": MODEL_DIR / "recyclable.onnx",
#     "harmful":    MODEL_DIR / "harmful.onnx",
# }

# # Stage 1 class ID → Stage 2 model name
# # Matches the REMAP dictionary used during training:
# #   0: Recyclable (original sub-class IDs 0-7)
# #   1: FoodWaste  (original sub-class IDs 8-10)
# #   2: Others     (original sub-class IDs 11-21)
# #   3: Harmful    (original sub-class IDs 22-34)
# ROOT_TO_MODEL = {
#     0: "recyclable",
#     1: "food",
#     2: "other",
#     3: "harmful",
# }

# # Human-readable category names for logging and output
# ROOT_CATEGORY_NAMES = {
#     0: "Recyclable",
#     1: "FoodWaste",
#     2: "Others",
#     3: "Harmful",
# }

# # =============================
# # LOAD ALL MODELS
# # =============================
# loaded_sessions = {}

# def load_all_models():
#     """Load all 5 ONNX models into memory at startup."""
#     try:
#         for model_name, model_path in MODEL_FILES.items():
#             if model_path.exists():
#                 session = ort.InferenceSession(
#                     str(model_path),
#                     providers=['CPUExecutionProvider']
#                 )
#                 loaded_sessions[model_name] = session
#                 print(f"✅ Loaded model: {model_name}")
#             else:
#                 print(f"⚠️  Model not found: {model_path}")
#                 loaded_sessions[model_name] = None
#     except Exception as e:
#         print(f"❌ Error loading models: {e}")

# load_all_models()

# # =============================
# # PREPROCESS IMAGE
# # =============================
# def preprocess_image(img, target_size=INPUT_SIZE):
#     """
#     Accepts: PIL Image, file path string, numpy array,
#              file-like object, or raw bytes.
#     Returns: float32 numpy array of shape (1, 3, 640, 640)
#              normalised to [0, 1], or None on failure.
#     """
#     try:
#         if isinstance(img, Image.Image):
#             pil_image = img

#         elif isinstance(img, str):
#             pil_image = Image.open(img)

#         elif isinstance(img, np.ndarray):
#             pil_image = Image.fromarray(img)

#         elif hasattr(img, 'read'):
#             import io
#             file_bytes = img.read()
#             pil_image = Image.open(io.BytesIO(file_bytes))
#             img.seek(0)

#         elif isinstance(img, bytes):
#             import io
#             pil_image = Image.open(io.BytesIO(img))

#         else:
#             print(f"⚠️  Unknown image type: {type(img)}")
#             return None

#         # Ensure RGB (drop alpha channel if present)
#         if pil_image.mode != 'RGB':
#             pil_image = pil_image.convert('RGB')

#         pil_image  = pil_image.resize(target_size, Image.Resampling.LANCZOS)
#         img_array  = np.array(pil_image, dtype=np.float32) / 255.0
#         img_array  = np.transpose(img_array, (2, 0, 1))   # HWC → CHW
#         img_array  = np.expand_dims(img_array, axis=0)    # CHW → BCHW
#         return img_array

#     except Exception as e:
#         print(f"❌ Error preprocessing image: {e}")
#         return None

# # =============================
# # PARSE YOLOv8 OUTPUT
# # =============================
# def parse_yolo_detection(output, num_classes):
#     """
#     Parse raw YOLOv8 ONNX output tensor.
#     Output shape expected: (4 + num_classes, num_anchors)
#     Returns: (class_id, confidence) or (None, None) on failure.
#     """
#     try:
#         if output.shape[0] < 5:
#             print(f"⚠️  Invalid output shape: {output.shape}")
#             return None, None

#         # Rows 0-3 are bbox coords, rows 4+ are class logits
#         class_scores = output[4:, :]

#         # Apply sigmoid to convert logits to probabilities
#         class_scores = 1 / (1 + np.exp(-class_scores))

#         # For each class, take the max score across all anchors
#         max_scores_per_class = np.max(class_scores, axis=1)

#         class_id   = int(np.argmax(max_scores_per_class))
#         confidence = float(max_scores_per_class[class_id])

#         return class_id, confidence

#     except Exception as e:
#         print(f"❌ Error parsing YOLO output: {e}")
#         return None, None

# # =============================
# # RUN INFERENCE
# # =============================
# def run_inference(session, input_data, num_classes):
#     """
#     Run a single ONNX session inference.
#     Returns: (class_id, confidence) or (None, None) on failure.
#     """
#     try:
#         input_name = session.get_inputs()[0].name
#         outputs    = session.run(None, {input_name: input_data})
#         raw_output = outputs[0][0]
#         return parse_yolo_detection(raw_output, num_classes)

#     except Exception as e:
#         print(f"❌ Inference error: {e}")
#         return None, None

# # =============================
# # HIERARCHICAL PREDICTION
# # =============================
# def predict_image(img, return_confidence=False):
#     """
#     Full two-stage hierarchical classification.

#     Stage 1: root model → one of 4 main categories
#     Stage 2: specialist model → exact sub-class

#     Args:
#         img:               image in any supported format (see preprocess_image)
#         return_confidence: if True, returns (waste_type, bin_type, confidence)
#                            if False, returns (waste_type, bin_type)

#     Returns:
#         waste_type:  string sub-class name e.g. "Cardboard", "Batteries"
#         bin_type:    string bin target e.g. "recycling", "harmful"
#         confidence:  float 0-1 (only if return_confidence=True)
#     """
#     try:
#         # Guard: root model must be loaded
#         if "root" not in loaded_sessions or loaded_sessions["root"] is None:
#             print("⚠️  Root model not loaded — using fallback")
#             return fallback_prediction(return_confidence)

#         # Preprocess
#         processed_img = preprocess_image(img)
#         if processed_img is None:
#             print("⚠️  Preprocessing failed — using fallback")
#             return fallback_prediction(return_confidence)

#         # ── STAGE 1: ROOT CLASSIFICATION ──────────────────────
#         print("🔍 Stage 1: Running root classifier...")

#         root_class_id, root_confidence = run_inference(
#             loaded_sessions["root"],
#             processed_img,
#             num_classes=4
#         )

#         if root_class_id is None:
#             print("⚠️  Root classification failed — using fallback")
#             return fallback_prediction(return_confidence)

#         if root_confidence < CONFIDENCE_THRESHOLD_ROOT:
#             print(f"⚠️  Root confidence too low "
#                   f"({root_confidence:.2%} < {CONFIDENCE_THRESHOLD_ROOT:.0%}) "
#                   f"— using fallback")
#             return fallback_prediction(return_confidence)

#         if root_class_id not in ROOT_TO_MODEL:
#             print(f"⚠️  Invalid root class ID: {root_class_id} — using fallback")
#             return fallback_prediction(return_confidence)

#         category_model_name = ROOT_TO_MODEL[root_class_id]
#         category_label      = ROOT_CATEGORY_NAMES[root_class_id]
#         stage2_threshold    = CONFIDENCE_THRESHOLD_STAGE2.get(category_model_name, 0.25)

#         print(f"📌 Root Category: {category_label} / "
#               f"model={category_model_name} ({root_confidence:.2%})")

#         # ── STAGE 2: SPECIALIST CLASSIFICATION ───────────────
#         print(f"🔍 Stage 2: Running {category_model_name} classifier...")

#         if (category_model_name not in loaded_sessions
#                 or loaded_sessions[category_model_name] is None):
#             # Specialist model missing — fall back to category name only
#             print(f"⚠️  Specialist model '{category_model_name}' not loaded "
#                   f"— using category label")
#             waste_type = category_label
#             confidence = root_confidence

#         else:
#             num_specific_classes = len(
#                 CLASS_MAPPING.get(category_model_name, {})
#             )

#             specific_class_id, specific_confidence = run_inference(
#                 loaded_sessions[category_model_name],
#                 processed_img,
#                 num_classes=num_specific_classes
#             )

#             if specific_class_id is None:
#                 # Inference failed — fall back to category
#                 print("⚠️  Stage 2 inference failed — using category label")
#                 waste_type = category_label
#                 confidence = root_confidence

#             elif specific_confidence < stage2_threshold:
#                 # Below per-category threshold — still use sub-class label
#                 # but log the low confidence so the IoT team can monitor it
#                 waste_type = CLASS_MAPPING.get(
#                     category_model_name, {}
#                 ).get(specific_class_id, category_label)
#                 confidence = specific_confidence
#                 print(f"⚠️  Stage 2 confidence low "
#                       f"({specific_confidence:.2%} < {stage2_threshold:.0%}) "
#                       f"— keeping sub-class '{waste_type}' but flagging")

#             else:
#                 waste_type = CLASS_MAPPING.get(
#                     category_model_name, {}
#                 ).get(specific_class_id, category_label)
#                 confidence = specific_confidence
#                 print(f"📌 Specific Type: {waste_type} ({specific_confidence:.2%})")

#         # ── RESOLVE BIN ───────────────────────────────────────
#         bin_type = get_bin_type(waste_type)
#         print(f"✅ Final Prediction: {waste_type} → {bin_type}")

#         if return_confidence:
#             return waste_type, bin_type, confidence
#         return waste_type, bin_type

#     except Exception as e:
#         print(f"❌ Prediction error: {e}")
#         import traceback
#         traceback.print_exc()
#         return fallback_prediction(return_confidence)

# # =============================
# # FALLBACK
# # =============================
# def fallback_prediction(return_confidence=False):
#     """
#     Returns a random valid prediction when the model pipeline fails.
#     Used only as a last resort — check logs for root cause.
#     """
#     waste     = random.choice(list(WASTE_TO_BIN.keys()))
#     bin_type  = get_bin_type(waste)
#     confidence = random.uniform(0.5, 0.9)
#     print(f"⚠️  Using fallback (random): {waste} → {bin_type}")
#     if return_confidence:
#         return waste, bin_type, confidence
#     return waste, bin_type

# code diatas code yang work waktu di integrasi.
import numpy as np
from PIL import Image
import cv2
import random
from pathlib import Path
import onnxruntime as ort
import warnings
import time
import csv
from datetime import datetime

warnings.filterwarnings("ignore", message=".*torch.classes.*")

from core.classification.labels import (
    CLASS_MAPPING,
    WASTE_TO_BIN,
    BIN_TYPES,
    get_bin_type
)

# =============================
# CONFIGURATION
# =============================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_DIR = BASE_DIR / "models"
LOG_DIR = BASE_DIR / "logs"

# Pastikan folder logs ada
LOG_DIR.mkdir(parents=True, exist_ok=True)

# File path untuk latency log
LATENCY_LOG_FILE = LOG_DIR / "inference_latency.csv"

INPUT_SIZE = (640, 640)

# Per-stage confidence thresholds
CONFIDENCE_THRESHOLD_ROOT = 0.30
CONFIDENCE_THRESHOLD_STAGE2 = {
    "recyclable": 0.25,
    "food":       0.25,
    "other":      0.15,
    "harmful":    0.15,
}

MODEL_FILES = {
    "root":       MODEL_DIR / "root.onnx",
    "food":       MODEL_DIR / "food.onnx",
    "other":      MODEL_DIR / "other.onnx",
    "recyclable": MODEL_DIR / "recyclable.onnx",
    "harmful":    MODEL_DIR / "harmful.onnx",
}

ROOT_TO_MODEL = {
    0: "recyclable",
    1: "food",
    2: "other",
    3: "harmful",
}

ROOT_CATEGORY_NAMES = {
    0: "Recyclable",
    1: "FoodWaste",
    2: "Others",
    3: "Harmful",
}

# =============================
# LOAD ALL MODELS
# =============================
loaded_sessions = {}

def load_all_models():
    """Load all 5 ONNX models into memory at startup."""
    for model_name, model_path in MODEL_FILES.items():
        if model_path.exists():
            session = ort.InferenceSession(
                str(model_path),
                providers=['CPUExecutionProvider']
            )
            loaded_sessions[model_name] = session
            print(f"✅ Loaded model: {model_name}")
        else:
            print(f"⚠️  Model not found: {model_path}")
            loaded_sessions[model_name] = None

load_all_models()

# =============================
# CSV LOGGING FUNCTION
# =============================
def save_latency_to_csv(latencies, waste_type, bin_type, confidence, 
                        root_category, root_confidence, stage2_model, stage2_confidence):
    """
    Save latency metrics to CSV file in logs folder
    """
    try:
        # Check if file exists to write header
        file_exists = LATENCY_LOG_FILE.exists()
        
        with open(LATENCY_LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            
            # Write header if file is new
            if not file_exists:
                writer.writerow([
                    "timestamp",
                    "waste_type",
                    "bin_type",
                    "confidence",
                    "root_category",
                    "root_confidence",
                    "stage2_model",
                    "stage2_confidence",
                    "preprocessing_ms",
                    "stage1_inference_ms",
                    "stage2_inference_ms",
                    "total_inference_ms",
                    "overall_latency_ms"
                ])
            
            # Write data row
            writer.writerow([
                datetime.now().isoformat(),
                waste_type,
                bin_type,
                f"{confidence:.4f}",
                root_category,
                f"{root_confidence:.4f}",
                stage2_model,
                f"{stage2_confidence:.4f}" if stage2_confidence is not None else "N/A",
                f"{latencies['preprocessing']:.2f}",
                f"{latencies['stage1_inference']:.2f}",
                f"{latencies['stage2_inference']:.2f}",
                f"{latencies['stage1_inference'] + latencies['stage2_inference']:.2f}",
                f"{latencies['total']:.2f}"
            ])
        
        print(f"💾 Latency data saved to: {LATENCY_LOG_FILE}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving latency log: {e}")
        return False

# =============================
# PREPROCESS IMAGE
# =============================
def preprocess_image(img, target_size=INPUT_SIZE):
    """Preprocess image and return tensor, also track time"""
    start_time = time.time()
    
    try:
        if isinstance(img, Image.Image):
            pil_image = img
        elif isinstance(img, str):
            pil_image = Image.open(img)
        elif isinstance(img, np.ndarray):
            pil_image = Image.fromarray(img)
        elif hasattr(img, 'read'):
            import io
            file_bytes = img.read()
            pil_image = Image.open(io.BytesIO(file_bytes))
            img.seek(0)
        elif isinstance(img, bytes):
            import io
            pil_image = Image.open(io.BytesIO(img))
        else:
            print(f"⚠️  Unknown image type: {type(img)}")
            return None, 0.0

        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')

        pil_image  = pil_image.resize(target_size, Image.Resampling.LANCZOS)
        img_array  = np.array(pil_image, dtype=np.float32) / 255.0
        img_array  = np.transpose(img_array, (2, 0, 1))
        img_array  = np.expand_dims(img_array, axis=0)
        
        elapsed = (time.time() - start_time) * 1000  # ms
        return img_array, elapsed

    except Exception as e:
        print(f"❌ Error preprocessing image: {e}")
        return None, 0.0

def parse_yolo_detection(output, num_classes):
    """Parse raw YOLOv8 ONNX output tensor."""
    try:
        if output.shape[0] < 5:
            print(f"⚠️  Invalid output shape: {output.shape}")
            return None, None

        class_scores = output[4:, :]
        class_scores = 1 / (1 + np.exp(-class_scores))
        max_scores_per_class = np.max(class_scores, axis=1)
        class_id   = int(np.argmax(max_scores_per_class))
        confidence = float(max_scores_per_class[class_id])

        return class_id, confidence

    except Exception as e:
        print(f"❌ Error parsing YOLO output: {e}")
        return None, None

def run_inference(session, input_data, num_classes):
    """Run inference and track time"""
    start_time = time.time()
    
    try:
        input_name = session.get_inputs()[0].name
        outputs    = session.run(None, {input_name: input_data})
        raw_output = outputs[0][0]
        
        elapsed = (time.time() - start_time) * 1000  # ms
        result = parse_yolo_detection(raw_output, num_classes)
        return result[0], result[1], elapsed

    except Exception as e:
        print(f"❌ Inference error: {e}")
        return None, None, 0.0

# =============================
# HIERARCHICAL PREDICTION WITH LATENCY
# =============================
def predict_image(img, return_confidence=False):
    """
    Full two-stage hierarchical classification with latency tracking.
    
    Returns:
        waste_type:  string sub-class name
        bin_type:    string bin target
        confidence:  float 0-1 (if return_confidence=True)
    
    Also prints latency metrics to console and saves to CSV.
    """
    total_start = time.time()
    
    # Latency tracking dictionary
    latencies = {
        "preprocessing": 0.0,
        "stage1_inference": 0.0,
        "stage2_inference": 0.0,
        "total": 0.0
    }
    
    # Variables for CSV logging
    root_category = "N/A"
    root_confidence = 0.0
    stage2_model = "N/A"
    stage2_confidence = None
    
    try:
        # Guard: root model must be loaded
        if "root" not in loaded_sessions or loaded_sessions["root"] is None:
            print("⚠️  Root model not loaded — using fallback")
            return fallback_prediction(return_confidence)

        # ── PREPROCESSING ───────────────────────────────
        processed_img, preproc_time = preprocess_image(img)
        latencies["preprocessing"] = preproc_time
        
        if processed_img is None:
            print("⚠️  Preprocessing failed — using fallback")
            return fallback_prediction(return_confidence)

        # ── STAGE 1: ROOT CLASSIFICATION ────────────────
        print("🔍 Stage 1: Running root classifier...")
        root_class_id, root_confidence, stage1_time = run_inference(
            loaded_sessions["root"],
            processed_img,
            num_classes=4
        )
        latencies["stage1_inference"] = stage1_time
        root_category = ROOT_CATEGORY_NAMES.get(root_class_id, "Unknown") if root_class_id is not None else "Unknown"

        if root_class_id is None:
            print("⚠️  Root classification failed — using fallback")
            return fallback_prediction(return_confidence)

        if root_confidence < CONFIDENCE_THRESHOLD_ROOT:
            print(f"⚠️  Root confidence too low "
                  f"({root_confidence:.2%} < {CONFIDENCE_THRESHOLD_ROOT:.0%})")
            return fallback_prediction(return_confidence)

        if root_class_id not in ROOT_TO_MODEL:
            print(f"⚠️  Invalid root class ID: {root_class_id}")
            return fallback_prediction(return_confidence)

        category_model_name = ROOT_TO_MODEL[root_class_id]
        category_label      = ROOT_CATEGORY_NAMES[root_class_id]
        stage2_threshold    = CONFIDENCE_THRESHOLD_STAGE2.get(category_model_name, 0.25)
        stage2_model = category_model_name

        print(f"📌 Root Category: {category_label} ({root_confidence:.2%})")

        # ── STAGE 2: SPECIALIST CLASSIFICATION ──────────
        print(f"🔍 Stage 2: Running {category_model_name} classifier...")

        if (category_model_name not in loaded_sessions
                or loaded_sessions[category_model_name] is None):
            print(f"⚠️  Specialist model '{category_model_name}' not loaded")
            waste_type = category_label
            confidence = root_confidence
            latencies["stage2_inference"] = 0.0

        else:
            num_specific_classes = len(
                CLASS_MAPPING.get(category_model_name, {})
            )

            specific_class_id, specific_confidence, stage2_time = run_inference(
                loaded_sessions[category_model_name],
                processed_img,
                num_classes=num_specific_classes
            )
            latencies["stage2_inference"] = stage2_time
            stage2_confidence = specific_confidence

            if specific_class_id is None:
                print("⚠️  Stage 2 inference failed")
                waste_type = category_label
                confidence = root_confidence

            elif specific_confidence < stage2_threshold:
                waste_type = CLASS_MAPPING.get(
                    category_model_name, {}
                ).get(specific_class_id, category_label)
                confidence = specific_confidence
                print(f"⚠️  Stage 2 confidence low ({specific_confidence:.2%})")

            else:
                waste_type = CLASS_MAPPING.get(
                    category_model_name, {}
                ).get(specific_class_id, category_label)
                confidence = specific_confidence
                print(f"📌 Specific Type: {waste_type} ({specific_confidence:.2%})")

        # ── RESOLVE BIN ─────────────────────────────────
        bin_type = get_bin_type(waste_type)
        
        # ── TOTAL LATENCY ───────────────────────────────
        latencies["total"] = (time.time() - total_start) * 1000  # ms
        
        # =============================
        # OUTPUT LATENCY DATA FOR JOURNAL
        # =============================
        print("\n" + "="*60)
        print("📊 INFERENCE LATENCY REPORT")
        print("="*60)
        print(f"├─ Preprocessing:     {latencies['preprocessing']:.2f} ms")
        print(f"├─ Stage 1 (root):    {latencies['stage1_inference']:.2f} ms")
        print(f"├─ Stage 2 ({category_model_name}): {latencies['stage2_inference']:.2f} ms")
        print(f"├─ Total inference:   {latencies['stage1_inference'] + latencies['stage2_inference']:.2f} ms")
        print(f"└─ Overall latency:   {latencies['total']:.2f} ms")
        print("="*60)
        print(f"✅ Prediction: {waste_type} → {bin_type} (conf: {confidence:.2%})")
        print("="*60 + "\n")
        
        # =============================
        # SAVE TO CSV
        # =============================
        save_latency_to_csv(
            latencies=latencies,
            waste_type=waste_type,
            bin_type=bin_type,
            confidence=confidence,
            root_category=root_category,
            root_confidence=root_confidence,
            stage2_model=stage2_model,
            stage2_confidence=stage2_confidence
        )

        if return_confidence:
            return waste_type, bin_type, confidence
        return waste_type, bin_type

    except Exception as e:
        print(f"❌ Prediction error: {e}")
        import traceback
        traceback.print_exc()
        return fallback_prediction(return_confidence)

# =============================
# FALLBACK
# =============================
def fallback_prediction(return_confidence=False):
    """Fallback random prediction when model pipeline fails."""
    waste     = random.choice(list(WASTE_TO_BIN.keys()))
    bin_type  = get_bin_type(waste)
    confidence = random.uniform(0.5, 0.9)
    print(f"⚠️  Using fallback (random): {waste} → {bin_type}")
    if return_confidence:
        return waste, bin_type, confidence
    return waste, bin_type