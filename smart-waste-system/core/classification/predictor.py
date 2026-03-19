
# ----------- core/classification/predictor.py -----------
import random

CLASSES = [
    "cardboard", "food organics", "glass", "metal",
    "miscellaneous trash", "paper", "plastic",
    "textile trash", "vegetation"
]

CLASS_MAPPING = {
    "cardboard": "recycling",
    "paper": "recycling",
    "plastic": "recycling",
    "glass": "recycling",
    "metal": "recycling",
    "food organics": "food_waste",
    "vegetation": "food_waste",
    "miscellaneous trash": "other",
    "textile trash": "other"
}


def predict_image(img):
    waste = random.choice(CLASSES)
    bin_type = CLASS_MAPPING.get(waste, "other")
    return waste, bin_type

