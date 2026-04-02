# ----------- core/mqtt/listener.py -----------
import paho.mqtt.client as mqtt
import json
import time
import threading
from queue import Queue

# Global queue untuk komunikasi dengan Streamlit
message_queue = Queue()
weight_queue = Queue()  # Queue khusus untuk weight status dari ESP32

class MQTTListener:
    def __init__(self, broker="localhost", port=1883):
        self.broker = broker
        self.port = port
        self.client = None
        self.running = False
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("✅ MQTT Listener Connected")
            # Subscribe ke topic yang diperlukan
            client.subscribe("smartwaste/user/id")      # Auto login
            client.subscribe("smartwaste/user/weight")  # Weight status dari ESP32
            client.subscribe("smart_waste/bin")         # Status bin (opsional)
            print("📡 Subscribed to topics: smartwaste/user/id, smartwaste/user/weight, smart_waste/bin")
        else:
            print(f"❌ MQTT Connection failed: {rc}")
    
    def on_message(self, client, userdata, msg):
        """Callback MQTT - jalan di thread sendiri"""
        try:
            if msg.retain:
                return  # Ignore retained messages
                
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            print(f"📥 MQTT Listener received on {topic}: {payload}")
            
            # =============================
            # HANDLE AUTO LOGIN (smartwaste/user/id)
            # =============================
            if topic == "smartwaste/user/id":
                if "user_id" in payload:
                    message_queue.put({
                        'user_id': str(payload['user_id']),
                        'userHashId': payload.get('userHashId'),
                        'statusTransaction': payload.get('statusTransaction'),
                        'timestamp': time.time()
                    })
                    print(f"✅ User ID queued: {payload['user_id']}")
            
            # =============================
            # HANDLE WEIGHT STATUS DARI ESP32 (smartwaste/user/weight)
            # =============================
            elif topic == "smartwaste/user/weight":
                weight_data = {
                    'topic': 'weight',
                    'user_id': payload.get('user_id'),
                    'user_hash': payload.get('user_hash'),
                    'waste_type': payload.get('waste_type'),
                    'bin_type': payload.get('bin_type'),
                    'weight_status': payload.get('weight_status', False),
                    'source': payload.get('source', 'esp32'),
                    'timestamp': payload.get('timestamp', time.time())
                }
                weight_queue.put(weight_data)
                print(f"⚖️ Weight status queued: {weight_data['weight_status']} from {weight_data['bin_type']}")
            
            # =============================
            # HANDLE BIN STATUS (smart_waste/bin) - Opsional
            # =============================
            elif topic == "smart_waste/bin":
                bin_data = {
                    'topic': 'bin',
                    'state': payload.get('state'),
                    'bin_type': payload.get('bin_type'),
                    'waste_type': payload.get('waste_type'),
                    'duration': payload.get('duration'),
                    'weight_status': payload.get('weight_status'),
                    'timestamp': payload.get('timestamp', time.time())
                }
                message_queue.put(bin_data)
                print(f"🗑️ Bin status queued: {bin_data['state']} - {bin_data['bin_type']}")
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
        except Exception as e:
            print(f"❌ MQTT Listener error: {e}")
    
    def start(self):
        """Jalankan MQTT listener di thread terpisah"""
        if self.running:
            return
            
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
        try:
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            self.running = True
            print("🚀 MQTT Listener thread started")
        except Exception as e:
            print(f"❌ Failed to start MQTT listener: {e}")
    
    def stop(self):
        """Hentikan listener"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.running = False
            print("🛑 MQTT Listener stopped")

# Singleton instance
_listener = None

def get_listener():
    """Dapatkan instance listener (singleton)"""
    global _listener
    if _listener is None:
        _listener = MQTTListener()
        _listener.start()
    return _listener

def get_messages():
    """Ambil semua pesan dari queue (non-blocking)"""
    messages = []
    while not message_queue.empty():
        try:
            messages.append(message_queue.get_nowait())
        except:
            break
    return messages

def get_weight_messages():
    """
    Ambil semua pesan weight status dari queue khusus.
    Digunakan untuk mendapatkan weight_status dari ESP32.
    """
    messages = []
    while not weight_queue.empty():
        try:
            messages.append(weight_queue.get_nowait())
        except:
            break
    return messages

def get_last_weight_status():
    """
    Ambil weight status terbaru dari ESP32.
    Mengembalikan None jika tidak ada.
    """
    messages = get_weight_messages()
    if messages:
        return messages[-1]  # Kembalikan yang terakhir
    return None


# =============================
# FUNGSI KHUSUS UNTUK WEIGHT SENSOR
# =============================

def wait_for_weight_status(timeout=30):
    """
    Tunggu weight status dari ESP32 dengan timeout.
    Returns: weight_status (bool) atau None jika timeout.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        weight_data = get_last_weight_status()
        if weight_data and weight_data.get('weight_status') is not None:
            return weight_data.get('weight_status')
        time.sleep(0.5)
    return None


def get_weight_status_sync():
    """
    Sinkronisasi weight status - ambil semua weight message yang masuk.
    """
    return get_weight_messages()