# ----------- test_model.py -----------
import os
import sys
from PIL import Image
import numpy as np

from core.classification.predictor import predict_image

def test_with_sample():
    """Test with a sample image"""
    print("🧪 Testing model with sample image...")
    
    # Create a dummy test image if none exists
    test_dir = "data/test_images"
    os.makedirs(test_dir, exist_ok=True)
    
    test_image_path = os.path.join(test_dir, "test.jpg")
    
    if not os.path.exists(test_image_path):
        # Create a dummy image
        img = Image.new('RGB', (224, 224), color='green')
        img.save(test_image_path)
        print(f"📸 Created test image: {test_image_path}")
    
    # Load and predict
    img = Image.open(test_image_path)
    waste, bin_type, confidence = predict_image(img, return_confidence=True)
    
    print("\n✅ Test Result:")
    print(f"   Waste Type: {waste}")
    print(f"   Bin Type: {bin_type}")
    print(f"   Confidence: {confidence:.2%}")

if __name__ == "__main__":
    test_with_sample()