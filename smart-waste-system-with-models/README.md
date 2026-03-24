## 📝 **Updated README.md**

```markdown
# ♻️ Smart Waste Management System (SWMS)

A comprehensive IoT-based smart waste management system with AI-powered waste classification, MQTT integration, and blockchain-ready architecture.

## 🚀 Features

### Core Features
- **AI Waste Classification** - Multi-stage hierarchical classification using YOLOv8 ONNX models
- **Real-time MQTT Communication** - Publish/Subscribe architecture for IoT integration
- **User Authentication** - Secure login via MQTT (User Hash ID) or manual barcode
- **Session Management** - Auto timeout and session tracking
- **Weight Sensor Integration** - User confirmation flag for blockchain verification

### System Components
- **User Mode** - Interactive waste disposal interface with camera/upload options
- **Admin Mode** - Testing and override capabilities
- **Dashboard** - Real-time monitoring and analytics
- **Digital Twin** - Virtual representation of physical bins

### Technical Specifications
- **AI Models**: YOLOv8 ONNX (root + specialist models)
- **ML Framework**: TensorFlow 2.16+, ONNX Runtime
- **MQTT Broker**: Mosquitto / any MQTT 3.1.1 compliant broker
- **Frontend**: Streamlit
- **Database**: CSV-based logging (transactions, latency metrics)

## 📋 Prerequisites

- Python 3.9+
- MQTT Broker (e.g., Mosquitto)
- Webcam (for camera capture)
- macOS / Linux / Windows

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/amirakbarwicaksono/smart-waste-uncc.git
cd smart-waste-uncc
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup MQTT Broker
```bash
# Install Mosquitto (macOS)
brew install mosquitto

# Start Mosquitto
mosquitto -c /opt/homebrew/etc/mosquitto/mosquitto.conf
```

### 5. Place AI Models
Download the following ONNX models and place them in `models/`:
- `root.onnx` - Stage 1 classifier (4 categories)
- `food.onnx` - Food waste specialist
- `other.onnx` - Other waste specialist
- `recyclable.onnx` - Recyclable waste specialist
- `harmful.onnx` - Harmful waste specialist

### 6. Run the Application
```bash
streamlit run app/main.py
```

## 📁 Project Structure

```
smart-waste-system/
├── app/
│   ├── main.py                 # Landing page & MQTT listener
│   └── pages/
│       ├── user_mode.py        # User disposal interface
│       ├── admin_mode.py       # Admin testing interface
│       ├── dashboard.py        # Real-time monitoring
│       └── digital_twin.py     # Virtual bin representation
├── core/
│   ├── barcode/                # Barcode scanner module
│   ├── camera/                 # Webcam capture module
│   ├── classification/         # AI prediction pipeline
│   │   ├── predictor.py        # Hierarchical inference
│   │   ├── labels.py           # Class mappings
│   │   └── model.py            # Model architecture
│   ├── bin_control/            # Hardware bin control
│   ├── mqtt/                   # MQTT client & listener
│   └── utils/                  # Utilities (timestamp, etc.)
├── logs/
│   ├── transactions.csv        # All disposal transactions
│   └── inference_latency.csv   # AI performance metrics
├── models/                     # ONNX model files
├── requirements.txt
└── README.md
```

## 📡 MQTT Topics

| Topic | Direction | Payload |
|-------|-----------|---------|
| `smartwaste/user/id` | Subscribe | `{"user_id": "xxx", "userHashId": "xxx", "statusTransaction": "running"}` |
| `smart_waste/bin` | Publish | `{"timestamp": "...", "barcode": "...", "waste_type": "...", "bin_type": "...", "state": "open/closed", "duration": 0, "weight_status": true/false}` |
| `smartwaste/user/timeout` | Publish | `{"user_id": "...", "user_hash": "...", "reason": "timeout/logout"}` |

## 🔐 Authentication Flow

1. **MQTT Auto-Login**: System subscribes to `smartwaste/user/id`
2. Upon receiving `{"userHashId": "...", "user_id": "...", "statusTransaction": "running"}`
3. User is redirected to User Mode with Hash ID as primary identifier
4. Optional: Manual barcode scan fallback

## 🤖 AI Prediction Flow

1. **Stage 1 - Root Classifier**: Classifies waste into 4 categories:
   - Recyclable (0)
   - FoodWaste (1)
   - Others (2)
   - Harmful (3)

2. **Stage 2 - Specialist Models**: Fine-grained classification within category
   - Confidence thresholds per category
   - Fallback to category name if confidence too low

3. **Output**: Waste type + Bin type mapping

## 📊 Data Logging

### Transactions CSV (`logs/transactions.csv`)
| Column | Description |
|--------|-------------|
| timestamp | ISO format timestamp |
| barcode | User Hash ID (or user_id fallback) |
| waste_type | AI-predicted waste type |
| bin_type | Target bin (recycling/food_waste/other/harmful) |
| bin_state | open / closed / weight_check |
| bin_duration_sec | Time bin was open |
| weight_status | User confirmation (true/false) |

### Inference Latency CSV (`logs/inference_latency.csv`)
| Column | Description |
|--------|-------------|
| timestamp | ISO format timestamp |
| waste_type | Predicted waste type |
| bin_type | Target bin |
| confidence | Model confidence score |
| preprocessing_ms | Image preprocessing time |
| stage1_inference_ms | Root model inference time |
| stage2_inference_ms | Specialist model inference time |
| overall_latency_ms | Total inference time |

## ⚙️ Configuration

### MQTT Broker Settings (`core/mqtt/client.py`)
```python
MQTT_BROKER = "localhost"  # Change to your broker IP
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
```

### Model Paths (`core/classification/predictor.py`)
```python
MODEL_FILES = {
    "root": MODEL_DIR / "root.onnx",
    "food": MODEL_DIR / "food.onnx",
    "other": MODEL_DIR / "other.onnx",
    "recyclable": MODEL_DIR / "recyclable.onnx",
    "harmful": MODEL_DIR / "harmful.onnx",
}
```

### Confidence Thresholds
```python
CONFIDENCE_THRESHOLD_ROOT = 0.30
CONFIDENCE_THRESHOLD_STAGE2 = {
    "recyclable": 0.25,
    "food": 0.25,
    "other": 0.15,
    "harmful": 0.15,
}
```

## 🧪 Testing

### Test MQTT Connection
```bash
# Publish test user
mosquitto_pub -t "smartwaste/user/id" -m '{"user_id": "test123", "userHashId": "test_hash_123", "statusTransaction": "running"}'

# Subscribe to bin status
mosquitto_sub -t "smart_waste/bin"
```

### Test Camera
```bash
python test_camera.py
```

### Test AI Prediction
```bash
python test_model.py
```

## 📈 Performance Metrics

- **Preprocessing Time**: ~6-12 ms
- **Stage 1 Inference**: ~650 ms (root model)
- **Stage 2 Inference**: ~350-400 ms (specialist)
- **Total Inference**: ~1,000-1,100 ms
- **End-to-end Latency**: ~1,020-1,100 ms

*Note: Performance measured on Apple M4*

## 🔧 Troubleshooting

### Common Issues

1. **MQTT Connection Failed**
   - Ensure broker is running: `mosquitto -v`
   - Check broker IP/port in `client.py`

2. **Camera Not Working**
   - Check camera permissions in browser
   - Test with `test_camera.py`
   - Use upload option as fallback

3. **Model Loading Error**
   - Verify ONNX models exist in `models/`
   - Check model file names match configuration

4. **Session Timeout Unexpectedly**
   - Adjust timeout in sidebar settings
   - Check `last_activity` updates in debug panel

## 📄 License

MIT License

## 👥 Contributors

- UNNC Exchange Students 2026
- IoT Research Team

## 🙏 Acknowledgments

- TensorFlow team for MobileNetV2
- ONNX Runtime for inference optimization
- Streamlit for web framework
```

---

## ✅ **README.md Updates**

| Section | Content |
|---------|---------|
| **Features** | AI classification, MQTT, authentication, weight sensor |
| **Technical Specs** | YOLOv8 ONNX, TensorFlow 2.16, Streamlit |
| **MQTT Topics** | Subscribe/publish topics with payload formats |
| **Authentication Flow** | Hash ID priority login |
| **AI Prediction Flow** | 2-stage hierarchical classification |
| **Data Logging** | CSV schema with weight_status |
| **Configuration** | Broker settings, model paths, thresholds |
| **Performance Metrics** | Latency breakdown |
| **Troubleshooting** | Common issues and solutions |

**README.md is ready!** 🚀