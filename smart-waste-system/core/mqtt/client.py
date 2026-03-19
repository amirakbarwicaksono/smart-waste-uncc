import paho.mqtt.client as mqtt
import json

BROKER = "localhost"   # change if needed
PORT = 1883
TOPIC = "smart_waste/bin"

client = mqtt.Client()

connected = False


def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        print("✅ MQTT Connected")
        connected = True
    else:
        print("❌ MQTT Connection Failed:", rc)


client.on_connect = on_connect


def connect_mqtt():
    global connected
    try:
        client.connect(BROKER, PORT, 60)
        client.loop_start()   # 🔥 VERY IMPORTANT

    except Exception as e:
        print("MQTT ERROR:", e)


def publish(data):
    if not connected:
        print("⚠️ MQTT not connected yet")
        return

    try:
        payload = json.dumps(data)
        result = client.publish(TOPIC, payload)

        if result.rc == 0:
            print("📡 Sent:", payload)
        else:
            print("❌ Failed to send")

    except Exception as e:
        print("MQTT Publish Error:", e)