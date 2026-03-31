# ♻️ Smart Waste Management System (SWMS)

A comprehensive IoT-based smart waste management system with AI-powered waste classification, MQTT integration, and blockchain-ready architecture.

## 🚀 Features

### Core Features
- **AI Waste Classification** - Multi-stage hierarchical classification using YOLOv8 ONNX models
- **Real-time MQTT Communication** - Publish/Subscribe architecture for IoT integration
- **User Authentication** - Secure login via MQTT (User Hash ID) or manual barcode
- **Session Management** - Auto timeout and session tracking
- **Weight Sensor Integration** - User confirmation flag for blockchain verification
- **Blockchain Simulation** - Motoko-style blockchain simulator with points system

### System Components
- **User Mode** - Interactive waste disposal interface with camera/upload options
- **Admin Mode** - Testing and override capabilities
- **Dashboard** - Real-time monitoring and analytics
- **Digital Twin** - Virtual representation of physical bins
- **Blockchain Dashboard** - Live transaction feed, points tracking, and analytics

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
- **Database**: CSV-based logging (transactions, latency metrics)
- **Blockchain**: Simulator mode (Motoko-ready architecture)

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
├── logs/
│   ├── transactions.csv        # All disposal transactions
│   ├── inference_latency.csv   # AI performance metrics
│   └── blockchain_ledger.json  # Blockchain ledger (simulator)
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
| `smartwaste/user/dispose` | Publish | `{"user_id": "...", "reason": "disposemore"}` |

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
- Transaction verification based on `weight_status`
- Points-based reward system

### Blockchain Flow
1. **Weight Confirmation**: User confirms if waste was actually disposed (`weight_status = true/false`)
2. **Transaction Filtering**: Only `weight_status = true` transactions are hashed to blockchain
3. **Points Reward**: Each verified transaction earns **0.5 points**
4. **Ledger Storage**: Transactions stored in `logs/blockchain_ledger.json`

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
- **Blockchain Transaction**: < 100 ms (simulator)

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

5. **Blockchain Transaction Not Recorded**
   - Ensure `weight_status = true` when confirming
   - Check `logs/blockchain_ledger.json` for entries
   - Verify `weight_status` is passed correctly in `user_mode.py`

## 🚀 Future Roadmap

- [ ] **Motoko Canister Deployment** - Migrate from simulator to actual Internet Computer canister
- [ ] **Internet Identity Integration** - Secure user authentication via II
- [ ] **Cycles Management** - Automated cycles replenishment
- [ ] **Cross-Canister Calls** - Integration with reward distribution canisters
- [ ] **NFT Rewards** - Mint NFT badges for eco-friendly users
- [ ] **Mobile App** - React Native companion app for waste tracking

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
```