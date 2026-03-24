# import paho.mqtt.client as mqtt
# import json

# BROKER = "localhost"   # change if needed
# PORT = 1883
# TOPIC = "smart_waste/bin"

# client = mqtt.Client()

# connected = False


# def on_connect(client, userdata, flags, rc):
#     global connected
#     if rc == 0:
#         print("✅ MQTT Connected")
#         connected = True
#     else:
#         print("❌ MQTT Connection Failed:", rc)


# client.on_connect = on_connect


# def connect_mqtt():
#     global connected
#     try:
#         client.connect(BROKER, PORT, 60)
#         client.loop_start()   # 🔥 VERY IMPORTANT

#     except Exception as e:
#         print("MQTT ERROR:", e)


# def publish(data):
#     if not connected:
#         print("⚠️ MQTT not connected yet")
#         return

#     try:
#         payload = json.dumps(data)
#         result = client.publish(TOPIC, payload)

#         if result.rc == 0:
#             print("📡 Sent:", payload)
#         else:
#             print("❌ Failed to send")

#     except Exception as e:
#         print("MQTT Publish Error:", e)
# #last code work 52
# # ----------- core/mqtt/client.py -----------
# import paho.mqtt.client as mqtt
# import json
# import time
# from threading import Thread

# # MQTT Configuration
# MQTT_BROKER = "localhost"  # atau IP broker Anda
# MQTT_PORT = 1883
# MQTT_KEEPALIVE = 60

# # Global client
# mqtt_client = None
# message_callbacks = {}
# _subscribed_topics = set()  # Track topics already subscribed

# def on_connect(client, userdata, flags, rc):
#     """Callback ketika connected ke broker"""
#     if rc == 0:
#         print("✅ MQTT Connected")
#     else:
#         print(f"❌ MQTT Connection failed with code {rc}")

# def on_message(client, userdata, msg):
#     """Callback ketika ada pesan masuk"""
#     try:
#         topic = msg.topic
#         payload = msg.payload.decode()
        
#         # Log pesan dengan info retain (tapi batasi frekuensinya)
#         if msg.retain:
#             print(f"📡 Received RETAINED message on {topic}")
#         else:
#             print(f"📡 Received message on {topic}")
        
#         # Panggil callback yang terdaftar untuk topic ini
#         if topic in message_callbacks:
#             for callback in message_callbacks[topic]:
#                 try:
#                     callback(client, userdata, msg)
#                 except Exception as e:
#                     print(f"❌ Error in callback for {topic}: {e}")
            
#     except Exception as e:
#         print(f"❌ Error processing message: {e}")

# def connect_mqtt():
#     """Connect ke MQTT broker"""
#     global mqtt_client
    
#     if mqtt_client is None:
#         mqtt_client = mqtt.Client()
#         mqtt_client.on_connect = on_connect
#         mqtt_client.on_message = on_message
        
#         try:
#             mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
#             mqtt_client.loop_start()
#             time.sleep(1)  # Tunggu koneksi
#         except Exception as e:
#             print(f"❌ MQTT Connection error: {e}")
#             mqtt_client = None
    
#     return mqtt_client

# def publish(topic, payload, retain=False):
#     """Publish message ke MQTT broker"""
#     global mqtt_client
    
#     if mqtt_client is None:
#         connect_mqtt()
    
#     if mqtt_client:
#         try:
#             if isinstance(payload, dict):
#                 payload = json.dumps(payload)
            
#             result = mqtt_client.publish(topic, payload, retain=retain)
#             if result.rc == mqtt.MQTT_ERR_SUCCESS:
#                 print(f"📡 Sent to {topic}")
#             else:
#                 print(f"❌ Failed to publish to {topic}")
#         except Exception as e:
#             print(f"❌ MQTT Publish error: {e}")

# def subscribe(topic, callback=None):
#     """Subscribe ke topic MQTT (hanya sekali)"""
#     global mqtt_client, message_callbacks, _subscribed_topics
    
#     if mqtt_client is None:
#         connect_mqtt()
    
#     if mqtt_client:
#         try:
#             # Subscribe hanya jika belum pernah
#             if topic not in _subscribed_topics:
#                 mqtt_client.subscribe(topic)
#                 _subscribed_topics.add(topic)
#                 print(f"📡 Subscribed to {topic}")
#             else:
#                 print(f"📡 Already subscribed to {topic}")
            
#             # Register callback jika ada
#             if callback:
#                 if topic not in message_callbacks:
#                     message_callbacks[topic] = []
#                 # Hindari duplikasi callback
#                 if callback not in message_callbacks[topic]:
#                     message_callbacks[topic].append(callback)
            
#         except Exception as e:
#             print(f"❌ MQTT Subscribe error: {e}")

# def disconnect_mqtt():
#     """Disconnect dari MQTT broker"""
#     global mqtt_client
    
#     if mqtt_client:
#         mqtt_client.loop_stop()
#         mqtt_client.disconnect()
#         print("✅ MQTT Disconnected")

# ----------- core/mqtt/client.py -----------
import paho.mqtt.client as mqtt
import json
import time
from threading import Thread

# MQTT Configuration
MQTT_BROKER = "localhost"  # atau IP broker Anda
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# Global client
mqtt_client = None
message_callbacks = {}
_subscribed_topics = set()  # Track topics already subscribed

def on_connect(client, userdata, flags, rc):
    """Callback ketika connected ke broker"""
    if rc == 0:
        print("✅ MQTT Connected")
    else:
        print(f"❌ MQTT Connection failed with code {rc}")

def on_message(client, userdata, msg):
    """Callback ketika ada pesan masuk"""
    try:
        topic = msg.topic
        payload = msg.payload.decode()
        
        # Log pesan dengan info retain (tapi batasi frekuensinya)
        if msg.retain:
            print(f"📡 Received RETAINED message on {topic}")
        else:
            print(f"📡 Received message on {topic}")
        
        # Panggil callback yang terdaftar untuk topic ini
        if topic in message_callbacks:
            for callback in message_callbacks[topic]:
                try:
                    callback(client, userdata, msg)
                except Exception as e:
                    print(f"❌ Error in callback for {topic}: {e}")
            
    except Exception as e:
        print(f"❌ Error processing message: {e}")

def connect_mqtt():
    """Connect ke MQTT broker"""
    global mqtt_client
    
    if mqtt_client is None:
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        
        try:
            mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
            mqtt_client.loop_start()
            time.sleep(1)  # Tunggu koneksi
        except Exception as e:
            print(f"❌ MQTT Connection error: {e}")
            mqtt_client = None
    
    return mqtt_client

def publish(topic, payload, retain=False):
    """Publish message ke MQTT broker"""
    global mqtt_client
    
    if mqtt_client is None:
        connect_mqtt()
    
    if mqtt_client:
        try:
            if isinstance(payload, dict):
                payload = json.dumps(payload)
            
            result = mqtt_client.publish(topic, payload, retain=retain)
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"📡 Sent to {topic}")
            else:
                print(f"❌ Failed to publish to {topic}")
        except Exception as e:
            print(f"❌ MQTT Publish error: {e}")

def subscribe(topic, callback=None):
    """Subscribe ke topic MQTT (hanya sekali)"""
    global mqtt_client, message_callbacks, _subscribed_topics
    
    if mqtt_client is None:
        connect_mqtt()
    
    if mqtt_client:
        try:
            # Subscribe hanya jika belum pernah
            if topic not in _subscribed_topics:
                mqtt_client.subscribe(topic)
                _subscribed_topics.add(topic)
                print(f"📡 Subscribed to {topic}")
            else:
                print(f"📡 Already subscribed to {topic}")
            
            # Register callback jika ada
            if callback:
                if topic not in message_callbacks:
                    message_callbacks[topic] = []
                # Hindari duplikasi callback
                if callback not in message_callbacks[topic]:
                    message_callbacks[topic].append(callback)
            
        except Exception as e:
            print(f"❌ MQTT Subscribe error: {e}")

def disconnect_mqtt():
    """Disconnect dari MQTT broker"""
    global mqtt_client
    
    if mqtt_client:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        print("✅ MQTT Disconnected")