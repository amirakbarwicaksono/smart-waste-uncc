# ----------- core/mqtt/listener.py -----------
import paho.mqtt.client as mqtt
import json
import time
import threading
from queue import Queue

# Global queue untuk komunikasi dengan Streamlit
message_queue = Queue()

class MQTTListener:
    def __init__(self, broker="localhost", port=1883):
        self.broker = broker
        self.port = port
        self.client = None
        self.running = False
        
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("✅ MQTT Listener Connected")
            # Subscribe ke topic
            client.subscribe("smartwaste/user/id")
        else:
            print(f"❌ MQTT Connection failed: {rc}")
    
    def on_message(self, client, userdata, msg):
        """Callback MQTT - jalan di thread sendiri"""
        try:
            if msg.retain:
                return  # Ignore retained messages
                
            payload = json.loads(msg.payload.decode())
            print(f"📥 MQTT Listener received: {payload}")
            
            if "user_id" in payload:
                # Masukkan ke queue (thread-safe)
                message_queue.put({
                    'user_id': str(payload['user_id']),
                    'timestamp': time.time()
                })
                print(f"✅ User ID queued: {payload['user_id']}")
                
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