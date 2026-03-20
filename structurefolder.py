import os

# Root project folder
root = "smart-waste-system"

# Folder structure
folders = [
    "app/pages",
    "core/barcode",
    "core/camera",
    "core/classification",
    "core/bin_control",
    "core/blockchain",
    "core/utils",
    "core/mqtt",
    "core/pipeline",
    "federated_learning",
    "data/raw",
    "data/processed",
    "data/test_images",
    "models",
    "config",
    "logs"
]

# Files to initialize (empty placeholders)
files = [
    "app/main.py",
    "app/pages/user_mode.py",
    "app/pages/admin_mode.py",
    "app/pages/dashboard.py",

    "core/barcode/scanner.py",
    "core/camera/webcam.py",
    "core/classification/model.py",
    "core/classification/predictor.py",
    "core/classification/labels.py",
    "core/bin_control/bin_logic.py",
    "core/blockchain/motoko_client.py",
    "core/blockchain/payload_formatter.py",
    "core/utils/timestamp.py",
    "core/utils/mqtt_handler.py",
    "core/mqtt/client.py",
    "core/mqtt/listener.py",
    "core/pipeline/processor.py",

    "federated_learning/client.py",
    "federated_learning/server.py",
    "federated_learning/aggregator.py",

    "config/settings.yaml",
    "requirements.txt",
    "README.md"
]

# Create folders
for folder in folders:
    path = os.path.join(root, folder)
    os.makedirs(path, exist_ok=True)

# Create files
for file in files:
    path = os.path.join(root, file)
    with open(path, "w") as f:
        pass

print("✅ Project structure created successfully!")