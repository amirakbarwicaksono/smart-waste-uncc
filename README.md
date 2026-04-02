# ♻️ Smart Waste Management System (SWMS)

A comprehensive IoT-based smart waste management system with AI-powered waste classification, MQTT integration, ESP32 hardware control, and blockchain-ready architecture.

## 🚀 Features

### Core Features
- **AI Waste Classification** - Multi-stage hierarchical classification using YOLOv8 ONNX models
- **Real-time MQTT Communication** - Publish/Subscribe architecture for IoT integration
- **ESP32 Hardware Integration** - Physical bin control with servo motors and weight sensors
- **User Authentication** - Secure login via MQTT (User Hash ID) or manual barcode
- **Session Management** - Auto timeout and session tracking
- **Weight Sensor Integration** - Real weight detection from ESP32 load cells
- **Blockchain Simulation** - Motoko-style blockchain simulator with points system

### System Components
- **User Mode** - Interactive waste disposal interface with camera/upload options
- **Admin Mode** - Testing and override capabilities
- **Dashboard** - Real-time monitoring and analytics
- **Digital Twin** - Virtual representation of physical bins
- **Blockchain Dashboard** - Live transaction feed, points tracking, and analytics
- **ESP32 Firmware** - Arduino code for 4 independent smart bins

### Hardware Integration (ESP32)
- **4 Independent Bins** - Recycling, Food Waste, Other, Harmful
- **Servo Motor Control** - Automatic bin opening/closing
- **Weight Sensor (HX711)** - Real waste detection using load cells
- **LED Status Indicators** - Visual feedback for bin status
- **MQTT Communication** - Reliable message exchange with broker

### Blockchain Features (Simulator)
- **Transaction Recording** - Immutable record of verified waste disposals
- **Points System** - 0.5 points per verified transaction
- **User Statistics** - Track total points and transaction history
- **Verification Logic** - Only `weight_status=True` transactions are hashed to blockchain
- **Live Dashboard** - Real-time charts, top contributors, transaction feed

### Technical Specifications
- **AI Models**: YOLOv8 ONNX (root + specialist models)
- **ML Framework**: TensorFlow 2.16+, ONNX Runtime
- **MQTT Broker**: Mosquitto / any MQTT 3.1.1 compliant broker
- **Frontend**: Streamlit
- **Hardware**: ESP32, Servo MG996R, HX711 + Load Cell
- **Database**: CSV-based logging (transactions, latency metrics)
- **Blockchain**: Simulator mode (Motoko-ready architecture)

## 📋 Prerequisites

### Software
- Python 3.9+
- MQTT Broker (e.g., Mosquitto)
- Arduino IDE (for ESP32 firmware)
- Webcam (for camera capture)
- macOS / Linux / Windows

### Hardware (Optional - for physical bins)
- 4x ESP32 Development Boards
- 4x Servo Motors (MG996R or SG90)
- 4x Load Cells (5kg-20kg) + HX711 amplifiers
- 4x RGB LEDs
- Power supplies (5V 2A)

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

### 6. Configure ESP32 (Optional)
1. Open Arduino IDE
2. Install libraries: `PubSubClient`, `ArduinoJson`, `HX711`
3. Update WiFi credentials in ESP32 code:
```cpp
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "192.168.1.100";  // Your broker IP
```
4. Upload to each ESP32 with appropriate `BIN_TYPE`

### 7. Run the Application
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
│       ├── digital_twin.py     # Virtual bin representation
│       └── blockchain_dashboard.py  # Blockchain analytics
├── core/
│   ├── barcode/                # Barcode scanner module
│   ├── camera/                 # Webcam capture module
│   ├── classification/         # AI prediction pipeline
│   │   ├── predictor.py        # Hierarchical inference
│   │   ├── labels.py           # Class mappings
│   │   └── model.py            # Model architecture
│   ├── bin_control/            # Hardware bin control
│   ├── mqtt/                   # MQTT client & listener
│   ├── blockchain/             # Blockchain integration
│   │   ├── simulator.py        # Blockchain simulator
│   │   ├── payload_formatter.py # Data formatting for blockchain
│   │   └── motoko_client.py    # Motoko-ready client wrapper
│   └── utils/                  # Utilities (timestamp, etc.)
├── esp32/                      # ESP32 firmware
│   └── ESP32_Recycling/
│       ├── ESP32_Recycling.ino # Recycling bin firmware
│       ├── ESP32_waste_food.ino # Food waste bin firmware
│       ├── ESP32_other.ino     # Other bin firmware
│       └── ESP32_harmful.ino   # Harmful bin firmware
├── logs/
│   ├── transactions.csv        # All disposal transactions
│   ├── inference_latency.csv   # AI performance metrics
│   └── blockchain_ledger.json  # Blockchain ledger (simulator)
├── models/                     # ONNX model files
├── requirements.txt
└── README.md
```

## 📡 MQTT Topics

| Topic | Direction | Payload | Source |
|-------|-----------|---------|--------|
| `smartwaste/user/id` | Subscribe | `{"user_id": "xxx", "userHashId": "xxx", "statusTransaction": "running"}` | RFID/Card Reader |
| `smart_waste/bin` | Publish | `{"timestamp": "...", "barcode": "...", "waste_type": "...", "bin_type": "...", "state": "open", "duration": 0}` | Streamlit (User Mode) |
| `smart_waste/bin` | Subscribe | - | ESP32 (all bins) |
| `smartwaste/user/weight` | Publish | `{"weight_status": true/false, "waste_type": "...", "bin_type": "...", "user_id": "..."}` | ESP32 (after weight detection) |
| `smartwaste/user/weight` | Subscribe | - | Streamlit (waiting for confirmation) |
| `smartwaste/user/timeout` | Publish | `{"user_id": "...", "reason": "timeout/logout"}` | Streamlit |
| `smartwaste/user/dispose` | Publish | `{"user_id": "...", "reason": "disposemore"}` | Streamlit |

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

## 🔗 Blockchain Integration

### Architecture
The system includes a **blockchain simulator** that mimics Motoko canister behavior. This design allows for:
- Seamless migration to actual Internet Computer blockchain
- Transaction verification based on `weight_status` from ESP32
- Points-based reward system

### Blockchain Flow
1. **AI Predict** → waste_type, bin_type
2. **MQTT Open** → command sent to ESP32
3. **ESP32 detects weight** → sends `weight_status` via MQTT
4. **Transaction Filtering** → Only `weight_status = true` transactions are hashed to blockchain
5. **Points Reward** → Each verified transaction earns **0.5 points**
6. **Ledger Storage** → Transactions stored in `logs/blockchain_ledger.json`

### Blockchain Data Structure
```json
{
  "transaction_id": "uuid",
  "timestamp": "ISO timestamp",
  "user": {
    "hash": "user_hash_id",
    "display_name": "user_display_name"
  },
  "waste": {
    "type": "Paper",
    "bin_type": "recycling"
  },
  "verification": {
    "weight_detected": true,
    "is_valid": true
  },
  "metrics": {
    "duration_seconds": 30.01,
    "points_earned": 0.5,
    "reward_reason": "weight_confirmed"
  },
  "hash": "sha256_hash"
}
```

### Blockchain Dashboard Features
- **Live Transaction Feed** - Real-time display of recent transactions
- **KPI Cards** - Total transactions, active users, total points, success rate
- **Daily Activity Chart** - Bar chart of transactions per day
- **Points Trend Chart** - Line chart of points earned over time
- **Waste Type Distribution** - Pie chart of verified waste types
- **Top Contributors** - Leaderboard of users with highest points
- **Blockchain Status** - Network status, block height, total value locked

## 📊 Data Logging

### Transactions CSV (`logs/transactions.csv`)
| Column | Description |
|--------|-------------|
| timestamp | ISO format timestamp |
| barcode | User Hash ID (or user_id fallback) |
| waste_type | AI-predicted waste type |
| bin_type | Target bin (recycling/food_waste/other/harmful) |
| bin_state | open / closed |
| bin_duration_sec | Time bin was open (default 30s) |
| weight_status | ESP32 weight detection (true/false/null) |

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

### Blockchain Ledger (`logs/blockchain_ledger.json`)
| Field | Description |
|-------|-------------|
| transactions | Array of verified transactions |
| stats | Total transactions, users, points |
| users | User-specific statistics |

## ⚙️ Configuration

### MQTT Broker Settings (`core/mqtt/client.py`)
```python
MQTT_BROKER = "localhost"  # Change to your broker IP
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60
```

### ESP32 Configuration (in Arduino code)
```cpp
#define BIN_TYPE "recycling"  // Change per bin
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "192.168.1.100";
#define WEIGHT_THRESHOLD 50  // grams
```

### Blockchain Settings (`core/blockchain/simulator.py`)
```python
LEDGER_FILE = BASE_DIR / "logs" / "blockchain_ledger.json"
POINTS_PER_TRANSACTION = 0.5  # Points reward per verified disposal
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

# Simulate weight status from ESP32
mosquitto_pub -t "smartwaste/user/weight" -m '{"weight_status": true, "waste_type": "Paper", "bin_type": "recycling", "user_id": "test"}'
```

### Test Camera
```bash
python test_camera.py
```

### Test AI Prediction
```bash
python test_model.py
```

### Test Blockchain Integration
```bash
# Check blockchain ledger
cat logs/blockchain_ledger.json

# Verify transaction count
python -c "from core.blockchain import get_client; print(get_client().get_system_stats())"
```

## 📈 Performance Metrics

- **Preprocessing Time**: ~6-12 ms
- **Stage 1 Inference**: ~650 ms (root model)
- **Stage 2 Inference**: ~350-400 ms (specialist)
- **Total Inference**: ~1,000-1,100 ms
- **End-to-end Latency**: ~1,020-1,100 ms
- **ESP32 Response Time**: ~2-3 seconds (weight detection + MQTT)
- **Blockchain Transaction**: < 100 ms (simulator)

*Note: Performance measured on Apple M4*

## 🔧 Troubleshooting

### Common Issues

1. **MQTT Connection Failed**
   - Ensure broker is running: `mosquitto -v`
   - Check broker IP/port in `client.py` and ESP32 code

2. **ESP32 Not Responding**
   - Verify WiFi credentials in ESP32 code
   - Check MQTT broker IP address
   - Monitor serial output (115200 baud)

3. **Weight Sensor Not Detecting**
   - Calibrate HX711 scale
   - Adjust `WEIGHT_THRESHOLD` value
   - Check load cell connections

4. **Camera Not Working**
   - Check camera permissions in browser
   - Test with `test_camera.py`
   - Use upload option as fallback

5. **Model Loading Error**
   - Verify ONNX models exist in `models/`
   - Check model file names match configuration

6. **Session Timeout Unexpectedly**
   - Adjust timeout in sidebar settings
   - Check `last_activity` updates in debug panel

7. **Blockchain Transaction Not Recorded**
   - Ensure ESP32 sends `weight_status = true`
   - Check `logs/blockchain_ledger.json` for entries
   - Verify MQTT messages on `smartwaste/user/weight` topic

## 🚀 Future Roadmap

- [ ] **Motoko Canister Deployment** - Migrate from simulator to actual Internet Computer canister
- [ ] **Internet Identity Integration** - Secure user authentication via II
- [ ] **Cycles Management** - Automated cycles replenishment
- [ ] **Cross-Canister Calls** - Integration with reward distribution canisters
- [ ] **NFT Rewards** - Mint NFT badges for eco-friendly users
- [ ] **Mobile App** - React Native companion app for waste tracking
- [ ] **Battery-powered ESP32** - Deep sleep mode for power efficiency
- [ ] **OTA Updates** - Over-the-air firmware updates for ESP32

## 📄 License

MIT License

## 👥 Contributors

- UNNC Exchange Students 2026
- IoT Research Team

## 🙏 Acknowledgments

- TensorFlow team for MobileNetV2
- ONNX Runtime for inference optimization
- Streamlit for web framework
- DFINITY for Internet Computer blockchain
- ESP32 community for excellent documentation

```
