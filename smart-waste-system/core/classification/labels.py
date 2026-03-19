# ----------- core/classification/labels.py -----------
# Waste type categories (9 classes)
WASTE_CLASSES = [
    "cardboard", 
    "food organics", 
    "glass", 
    "metal",
    "miscellaneous trash", 
    "paper", 
    "plastic",
    "textile trash", 
    "vegetation"
]

# Mapping to bin types (4 bins)
BIN_MAPPING = {
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

# Get bin type from waste class
def get_bin_type(waste_class):
    """Return bin type for given waste class"""
    return BIN_MAPPING.get(waste_class, "other")

# All bin types
BIN_TYPES = ["recycling", "food_waste", "other", "harmful"]