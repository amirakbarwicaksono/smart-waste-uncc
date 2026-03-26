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