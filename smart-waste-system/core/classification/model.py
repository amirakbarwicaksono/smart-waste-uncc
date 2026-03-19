# ----------- core/classification/model.py -----------
import tensorflow as tf
import os

def create_model(input_shape=(224, 224, 3), num_classes=9):
    """
    Create CNN model for waste classification
    """
    # Use MobileNetV2 as base
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    
    base_model.trainable = False
    
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=input_shape),
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    return model

def save_model(model, model_path):
    """Save trained model"""
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    model.save(model_path)
    print(f"✅ Model saved to {model_path}")

def load_trained_model(model_path):
    """Load trained model if exists"""
    if os.path.exists(model_path):
        print(f"📂 Loading model from {model_path}")
        return tf.keras.models.load_model(model_path)
    return None