# # ----------- core/classification/labels.py -----------
# # Waste type categories (9 classes)
# WASTE_CLASSES = [
#     "cardboard", 
#     "food organics", 
#     "glass", 
#     "metal",
#     "miscellaneous trash", 
#     "paper", 
#     "plastic",
#     "textile trash", 
#     "vegetation"
# ]

# # Mapping to bin types (4 bins)
# BIN_MAPPING = {
#     "cardboard": "recycling",
#     "paper": "recycling",
#     "plastic": "recycling",
#     "glass": "recycling",
#     "metal": "recycling",
#     "food organics": "food_waste",
#     "vegetation": "food_waste",
#     "miscellaneous trash": "other",
#     "textile trash": "other"
# }

# # Get bin type from waste class
# def get_bin_type(waste_class):
#     """Return bin type for given waste class"""
#     return BIN_MAPPING.get(waste_class, "other")

# # All bin types
# BIN_TYPES = ["recycling", "food_waste", "other", "harmful"]

# # ----------- core/classification/labels.py -----------

# BIN_TYPES = ["recycling", "food_waste", "other", "harmful"]

# # ✅ Match the original 35 sub-class IDs from training
# CLASS_MAPPING = {
#     # Recyclable (original IDs 0-7) → 8 classes
#     "recyclable": {
#         0: "Cardboard",
#         1: "GlassContainer",
#         2: "PlasticPackaging",
#         3: "PlasticBottle",
#         4: "Textile",
#         5: "GlassBottle",
#         6: "Paper",
#         7: "Metal",
#     },
#     # Food (original IDs 8-10) → 3 classes
#     "food": {
#         0: "Vegetation",
#         1: "KitchenWaste",
#         2: "FoodScraps",
#     },
#     # Other (original IDs 11-21) → 11 classes
#     "other": {
#         0: "Styrofoam",
#         1: "PlasticCuttery",
#         2: "Straw",
#         3: "SanitaryNapkin",
#         4: "Diapers",
#         5: "CeramicProduct",
#         6: "Toys",
#         7: "Book",
#         8: "Tissue",
#         9: "Others",
#         10: "DirtyItems",
#     },
#     # Harmful (original IDs 22-34) → 13 classes
#     "harmful": {
#         0: "Printer",
#         1: "Television",
#         2: "WashingMachine",
#         3: "PCB",
#         4: "Mouse",
#         5: "Keyboard",
#         6: "Microwave",
#         7: "Handphone",
#         8: "Bulb",
#         9: "Computer",
#         10: "Batteries",
#         11: "Pesticides",
#         12: "Paints",
#     },
# }

# WASTE_TO_BIN = {
#     # Recyclable
#     "Cardboard": "recycling",
#     "GlassContainer": "recycling",
#     "GlassBottle": "recycling",
#     "PlasticPackaging": "recycling",
#     "PlasticBottle": "recycling",
#     "Paper": "recycling",
#     "Metal": "recycling",
#     "Textile": "recycling",
#     "Book": "recycling",
#     # Food
#     "Vegetation": "food_waste",
#     "KitchenWaste": "food_waste",
#     "FoodScraps": "food_waste",
#     # Other
#     "Styrofoam": "other",
#     "PlasticCuttery": "other",
#     "Straw": "other",
#     "SanitaryNapkin": "other",
#     "Diapers": "other",
#     "CeramicProduct": "other",
#     "Toys": "other",
#     "Tissue": "other",
#     "Others": "other",
#     "DirtyItems": "other",
#     # Harmful
#     "Printer": "harmful",
#     "Television": "harmful",
#     "WashingMachine": "harmful",
#     "PCB": "harmful",
#     "Mouse": "harmful",
#     "Keyboard": "harmful",
#     "Microwave": "harmful",
#     "Handphone": "harmful",
#     "Bulb": "harmful",
#     "Computer": "harmful",
#     "Batteries": "harmful",
#     "Pesticides": "harmful",
#     "Paints": "harmful",
# }

# def get_bin_type(waste_type):
#     return WASTE_TO_BIN.get(waste_type, "other")

# =============================
# BIN TYPES
# =============================
BIN_TYPES = ["recycling", "food_waste", "other", "harmful"]

# =============================
# CLASS MAPPING
# Matches the data.yaml names[] from training exactly.
# Key   = specialist model name (matches MODEL_FILES keys in predictor.py)
# Value = {local_class_id: sub-class label string}
# =============================
CLASS_MAPPING = {

    # ── Recyclable specialist (YOLOv8m, nc=8) ──────────────
    # Trained on stage2_recyclable/data.yaml
    "recyclable": {
        0: "Cardboard",
        1: "GlassContainer",
        2: "PlasticPackaging",
        3: "PlasticBottle",
        4: "Textile",
        5: "GlassBottle",
        6: "Paper",
        7: "Metal",
    },

    # ── FoodWaste specialist (YOLOv8s, nc=3) ───────────────
    # Trained on stage2_food/data.yaml
    "food": {
        0: "Vegetation",
        1: "KitchenWaste",
        2: "FoodScraps",
    },

    # ── Others specialist (YOLOv8m, nc=11) ─────────────────
    # Trained on stage2_others/data.yaml
    "other": {
        0:  "Styrofoam",
        1:  "PlasticCutlery",
        2:  "Straw",
        3:  "SanitaryNapkin",
        4:  "Diapers",
        5:  "CeramicProduct",
        6:  "Toys",
        7:  "Book",
        8:  "Tissue",
        9:  "Others",
        10: "DirtyItems",
    },

    # ── Harmful specialist (YOLOv8l, nc=13) ────────────────
    # Trained on stage2_harmful/data.yaml
    "harmful": {
        0:  "Printer",
        1:  "Television",
        2:  "WashingMachine",
        3:  "PCB",
        4:  "Mouse",
        5:  "Keyboard",
        6:  "Microwave",
        7:  "Handphone",
        8:  "Bulb",
        9:  "Computer",
        10: "Batteries",
        11: "Pesticides",
        12: "Paints",
    },
}

# =============================
# WASTE → BIN ROUTING TABLE
# Maps every sub-class label to its physical bin target.
# Any label not listed here defaults to "other" via get_bin_type().
# =============================
WASTE_TO_BIN = {

    # ── Recyclable bin ──────────────────────────────────────
    "Cardboard":       "recycling",
    "GlassContainer":  "recycling",
    "GlassBottle":     "recycling",
    "PlasticPackaging":"recycling",
    "PlasticBottle":   "recycling",
    "Paper":           "recycling",
    "Metal":           "recycling",
    "Textile":         "recycling",
    "Book":            "recycling",   # paper-based, recyclable

    # ── FoodWaste bin ───────────────────────────────────────
    "Vegetation":      "food_waste",
    "KitchenWaste":    "food_waste",
    "FoodScraps":      "food_waste",

    # ── Others / General waste bin ──────────────────────────
    "Styrofoam":       "other",
    "PlasticCutlery":  "other",
    "Straw":           "other",
    "SanitaryNapkin":  "other",
    "Diapers":         "other",
    "CeramicProduct":  "other",
    "Toys":            "other",
    "Tissue":          "other",
    "Others":          "other",
    "DirtyItems":      "other",

    # ── Harmful / Hazardous bin ─────────────────────────────
    "Printer":         "harmful",
    "Television":      "harmful",
    "WashingMachine":  "harmful",
    "PCB":             "harmful",
    "Mouse":           "harmful",
    "Keyboard":        "harmful",
    "Microwave":       "harmful",
    "Handphone":       "harmful",
    "Bulb":            "harmful",
    "Computer":        "harmful",
    "Batteries":       "harmful",
    "Pesticides":      "harmful",
    "Paints":          "harmful",
}

# =============================
# HELPER FUNCTION
# =============================
def get_bin_type(waste_type: str) -> str:
    """
    Returns the bin target string for a given waste sub-class label.
    Defaults to "other" if the label is not in WASTE_TO_BIN.

    Args:
        waste_type: sub-class label e.g. "Batteries", "Cardboard"

    Returns:
        bin target string: "recycling", "food_waste", "other", or "harmful"
    """
    return WASTE_TO_BIN.get(waste_type, "other")