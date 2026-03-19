# ----------- train_model.py -----------
import os
import sys
import numpy as np
import tensorflow as tf
import json
import matplotlib.pyplot as plt
from datetime import datetime

# Import dari core
from core.classification.model import create_model, save_model
from core.classification.labels import WASTE_CLASSES

# Configuration
DATA_DIR = "data/raw"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20
MODEL_SAVE_PATH = "models/waste_classifier.h5"
CLASS_INDICES_PATH = "models/class_indices.json"

print("=" * 50)
print("🚀 WASTE CLASSIFICATION TRAINING")
print("=" * 50)
print(f"📂 Dataset: {DATA_DIR}")
print(f"📊 Classes: {WASTE_CLASSES}")
print(f"🎯 Image Size: {IMG_SIZE}")
print(f"📦 Batch Size: {BATCH_SIZE}")
print(f"🔄 Epochs: {EPOCHS}")
print(f"🤖 TensorFlow version: {tf.__version__}")
print("=" * 50)

# Check if dataset exists
if not os.path.exists(DATA_DIR):
    print(f"❌ Dataset folder {DATA_DIR} not found!")
    print("📁 Creating folder structure...")
    for category in WASTE_CLASSES:
        os.makedirs(os.path.join(DATA_DIR, category), exist_ok=True)
        print(f"   Created: {category}/")
    print(f"✅ Please add images to {DATA_DIR}/[category]/")
    exit(1)

# Data augmentation
print("\n🔄 Preparing data generators...")
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    validation_split=0.2
)

# Load training data
print("📚 Loading training data...")
train_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True,
    classes=WASTE_CLASSES
)

# Load validation data
validation_generator = train_datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=True,
    classes=WASTE_CLASSES
)

# Save class indices
print("\n💾 Saving class indices...")
with open(CLASS_INDICES_PATH, 'w') as f:
    json.dump(train_generator.class_indices, f)
print(f"✅ Class indices saved: {train_generator.class_indices}")

# Create model
print("\n🔧 Creating model...")
model = create_model(
    input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
    num_classes=len(WASTE_CLASSES)
)

# Compile model
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

print("\n📊 Model Summary:")
model.summary()

# Callbacks
callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),
    tf.keras.callbacks.ModelCheckpoint(
        'models/best_model.h5',
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=1e-6,
        verbose=1
    )
]

# Train model
print("\n🚀 Starting training...")
start_time = datetime.now()

history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=validation_generator,
    callbacks=callbacks,
    verbose=1
)

training_time = datetime.now() - start_time
print(f"\n⏱️ Training time: {training_time}")

# Save model
print("\n💾 Saving model...")
save_model(model, MODEL_SAVE_PATH)

# Plot training history
print("\n📈 Generating plots...")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Accuracy
axes[0].plot(history.history['accuracy'], label='Training', linewidth=2)
axes[0].plot(history.history['val_accuracy'], label='Validation', linewidth=2)
axes[0].set_title('Model Accuracy', fontsize=14)
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Loss
axes[1].plot(history.history['loss'], label='Training', linewidth=2)
axes[1].plot(history.history['val_loss'], label='Validation', linewidth=2)
axes[1].set_title('Model Loss', fontsize=14)
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('models/training_history.png', dpi=150, bbox_inches='tight')
print("✅ Training history saved to models/training_history.png")

# Show final metrics
print("\n" + "=" * 50)
print("📊 FINAL RESULTS")
print("=" * 50)
print(f"Training Accuracy: {history.history['accuracy'][-1]:.2%}")
print(f"Validation Accuracy: {history.history['val_accuracy'][-1]:.2%}")
print(f"Training Loss: {history.history['loss'][-1]:.4f}")
print(f"Validation Loss: {history.history['val_loss'][-1]:.4f}")
print("=" * 50)

print("\n🎉 Training complete!")
print(f"✅ Model saved to: {MODEL_SAVE_PATH}")
print(f"✅ Class indices saved to: {CLASS_INDICES_PATH}")

# Show plot
plt.show()