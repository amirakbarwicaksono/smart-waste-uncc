// ============================================================
// Smart Waste Bin - ESP32 Code
// Bin Type: RECYCLING
// Compatible with ESP32 Arduino Core 3.x
// ============================================================

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <HX711.h>

// ============================================================
// BIN CONFIGURATION
// ============================================================
#define BIN_TYPE "recycling"

// WiFi Credentials (GANTI DENGAN SSID DAN PASSWORD ANDA)
const char* ssid = "FTI-USAKTI";
const char* password = "trisakti2026";

// MQTT Broker
const char* mqtt_server = "10.24.81.14";  // Bisa diganti dengan broker lain
const int mqtt_port = 1883;

// MQTT Topics
const char* mqtt_topic_bin = "smart_waste/bin";
const char* mqtt_topic_weight = "smartwaste/user/weight";

// Pin Definitions
#define PIN_SERVO     13      // Servo signal pin (PWM)
#define PIN_HX711_DT  4       // HX711 Data pin
#define PIN_HX711_SCK 5       // HX711 Clock pin
#define PIN_LED_RED   14      // LED Red
#define PIN_LED_GREEN 12      // LED Green
#define PIN_LED_BLUE  27      // LED Blue

// Servo PWM Parameters (ESP32 Core 3.x)
#define SERVO_PIN     13      // Pin for servo
#define SERVO_FREQ    50      // 50Hz = 20ms period
#define SERVO_RES     12      // 12-bit resolution (0-4095)

// Servo Pulse Width (microseconds)
#define SERVO_MIN_US  500     // 0.5ms (0 degrees)
#define SERVO_MAX_US  2500    // 2.5ms (180 degrees)

// Convert microseconds to duty cycle
#define US_TO_DUTY(us) (((us) * (1 << SERVO_RES)) / 20000)

// Weight Sensor Parameters
#define WEIGHT_THRESHOLD 50   // Minimum weight (grams)
#define WEIGHT_SAMPLE_COUNT 5

// Bin Parameters
#define BIN_OPEN_DURATION 30  // Seconds

// ============================================================
// GLOBAL VARIABLES
// ============================================================
WiFiClient espClient;
PubSubClient client(espClient);
HX711 scale;

// State variables
bool isOpen = false;
bool isProcessing = false;
String currentWasteType = "";
String currentTransactionId = "";
String currentUserId = "";
String currentUserHash = "";
String lastMessageId = "";

// PWM channel for servo (ESP32 Core 3.x uses ledcAttach)
int servoChannel = 0;

// ============================================================
// LED CONTROL
// ============================================================
void setLED(String status) {
  if (status == "standby") {
    digitalWrite(PIN_LED_RED, LOW);
    digitalWrite(PIN_LED_GREEN, HIGH);
    digitalWrite(PIN_LED_BLUE, LOW);
    Serial.println("🔵 LED: Standby (Green)");
  } 
  else if (status == "active") {
    digitalWrite(PIN_LED_RED, LOW);
    digitalWrite(PIN_LED_GREEN, LOW);
    digitalWrite(PIN_LED_BLUE, HIGH);
    Serial.println("🔵 LED: Active (Blue)");
  } 
  else if (status == "error") {
    digitalWrite(PIN_LED_RED, HIGH);
    digitalWrite(PIN_LED_GREEN, LOW);
    digitalWrite(PIN_LED_BLUE, LOW);
    Serial.println("🔴 LED: Error (Red)");
  } 
  else if (status == "blink") {
    static unsigned long lastBlink = 0;
    static bool blinkState = false;
    if (millis() - lastBlink > 250) {
      lastBlink = millis();
      blinkState = !blinkState;
      digitalWrite(PIN_LED_RED, blinkState);
      digitalWrite(PIN_LED_GREEN, blinkState);
      digitalWrite(PIN_LED_BLUE, blinkState);
    }
  }
}

// ============================================================
// SERVO CONTROL (ESP32 Core 3.x)
// ============================================================
void initServo() {
  // ESP32 Core 3.x uses ledcAttach(pin, freq, resolution)
  ledcAttach(PIN_SERVO, SERVO_FREQ, SERVO_RES);
  
  // Set to closed position
  int duty = US_TO_DUTY(SERVO_MIN_US);
  ledcWrite(PIN_SERVO, duty);
  Serial.println("✅ Servo initialized (closed position)");
  Serial.printf("   Frequency: %d Hz, Resolution: %d bits\n", SERVO_FREQ, SERVO_RES);
}

void setServoAngle(int angle) {
  // Constrain angle to 0-180
  if (angle < 0) angle = 0;
  if (angle > 180) angle = 180;
  
  // Map angle to pulse width (500-2500 us)
  int pulseWidth = SERVO_MIN_US + (angle * (SERVO_MAX_US - SERVO_MIN_US) / 180);
  
  // Set PWM duty cycle
  int duty = US_TO_DUTY(pulseWidth);
  ledcWrite(PIN_SERVO, duty);
  
  Serial.printf("Servo angle: %d°, pulse: %d us, duty: %d\n", angle, pulseWidth, duty);
}

void openBin() {
  if (!isOpen) {
    Serial.println("📦 Opening bin...");
    setServoAngle(180);  // Open position
    isOpen = true;
    setLED("active");
  }
}

void closeBin() {
  if (isOpen) {
    Serial.println("🔒 Closing bin...");
    setServoAngle(0);    // Closed position
    isOpen = false;
    setLED("standby");
  }
}

// ============================================================
// WEIGHT SENSOR
// ============================================================
void calibrateScale() {
  Serial.println("⚖️ Calibrating scale...");
  Serial.println("Make sure no weight on the scale");
  delay(3000);
  
  scale.tare();
  Serial.println("✅ Scale tared");
}

float readWeight() {
  if (scale.is_ready()) {
    float weight = scale.get_units(WEIGHT_SAMPLE_COUNT);
    if (weight < 0) weight = 0;
    return weight;
  }
  return 0;
}

bool isWeightDetected() {
  float weight = readWeight();
  bool detected = (weight > WEIGHT_THRESHOLD);
  
  if (detected) {
    Serial.printf("⚖️ Weight detected: %.2f g\n", weight);
  } else {
    Serial.printf("⚖️ Weight: %.2f g\n", weight);
  }
  
  return detected;
}

// ============================================================
// MQTT PUBLISH (using JsonDocument - new ArduinoJson v7)
// ============================================================
void publishWeightStatus(bool weightDetected) {
  JsonDocument doc;  // Use JsonDocument instead of StaticJsonDocument
  
  doc["timestamp"] = millis() / 1000;
  doc["user_id"] = currentUserId;
  doc["user_hash"] = currentUserHash;
  doc["waste_type"] = currentWasteType;
  doc["bin_type"] = BIN_TYPE;
  doc["weight_status"] = weightDetected;
  doc["source"] = "esp32";
  doc["transaction_id"] = currentTransactionId;
  
  String output;
  serializeJson(doc, output);
  
  if (client.publish(mqtt_topic_weight, output.c_str())) {
    Serial.printf("📤 Weight status published: %s\n", weightDetected ? "TRUE" : "FALSE");
  } else {
    Serial.println("❌ Failed to publish weight status");
  }
}

void publishBinStatus(String state, float duration) {
  JsonDocument doc;  // Use JsonDocument instead of StaticJsonDocument
  
  doc["timestamp"] = millis() / 1000;
  doc["barcode"] = currentUserHash.isEmpty() ? currentUserId : currentUserHash;
  doc["waste_type"] = currentWasteType;
  doc["bin_type"] = BIN_TYPE;
  doc["state"] = state;
  doc["duration"] = duration;
  doc["transaction_id"] = currentTransactionId;
  
  String output;
  serializeJson(doc, output);
  
  if (client.publish(mqtt_topic_bin, output.c_str())) {
    Serial.printf("📤 Bin status published: %s\n", state.c_str());
  } else {
    Serial.println("❌ Failed to publish bin status");
  }
}

// ============================================================
// BIN OPERATION
// ============================================================
void processBinOperation() {
  Serial.println("🚮 Starting bin operation...");
  
  openBin();
  publishBinStatus("open", 0);
  
  // Wait for user to place waste
  Serial.println("⏳ Waiting for waste placement...");
  delay(2000);
  
  bool weightDetected = isWeightDetected();
  publishWeightStatus(weightDetected);
  
  // Keep bin open
  if (weightDetected) {
    Serial.printf("📦 Bin will stay open for %d seconds\n", BIN_OPEN_DURATION);
    for (int i = BIN_OPEN_DURATION; i > 0; i--) {
      Serial.printf("   Closing in %d seconds...\n", i);
      delay(1000);
    }
  } else {
    Serial.println("⚠️ No waste detected, closing bin early...");
    delay(2000);
  }
  
  closeBin();
  publishBinStatus("closed", BIN_OPEN_DURATION);
  
  Serial.println("✅ Bin operation complete");
  
  isProcessing = false;
  currentTransactionId = "";
  currentWasteType = "";
  currentUserId = "";
  currentUserHash = "";
}

// ============================================================
// MQTT CALLBACK
// ============================================================
void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.printf("📥 MQTT: %s\n", message.c_str());
  
  if (strcmp(topic, mqtt_topic_bin) != 0) return;
  
  JsonDocument doc;  // Use JsonDocument instead of StaticJsonDocument
  DeserializationError error = deserializeJson(doc, message);
  
  if (error) {
    Serial.printf("❌ JSON error: %s\n", error.c_str());
    return;
  }
  
  String targetBin = doc["bin_type"] | "";
  if (targetBin != BIN_TYPE) {
    Serial.printf("⏭️ Not for this bin\n");
    return;
  }
  
  if (isProcessing) {
    Serial.println("⏭️ Busy");
    return;
  }
  
  String state = doc["state"] | "";
  if (state == "open") {
    currentWasteType = doc["waste_type"] | "unknown";
    currentTransactionId = doc["transaction_id"] | "";
    currentUserId = doc["user_id"] | "";
    currentUserHash = doc["barcode"] | "";
    
    if (currentUserId.isEmpty()) currentUserId = currentUserHash;
    
    Serial.printf("🎯 Processing: %s\n", currentWasteType.c_str());
    
    isProcessing = true;
    setLED("blink");
    processBinOperation();
  }
}

// ============================================================
// MQTT RECONNECT
// ============================================================
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Connecting MQTT...");
    String clientId = "SmartBin-" + String(BIN_TYPE) + "-" + String(random(0xffff), HEX);
    
    if (client.connect(clientId.c_str())) {
      Serial.println("✅ Connected");
      client.subscribe(mqtt_topic_bin);
      setLED("standby");
    } else {
      Serial.print("❌ Failed, rc=");
      Serial.print(client.state());
      Serial.println(" retrying...");
      setLED("error");
      delay(5000);
    }
  }
}

// ============================================================
// WIFI SETUP
// ============================================================
void setupWiFi() {
  Serial.printf("Connecting to WiFi %s", ssid);
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("\n✅ WiFi connected, IP: %s\n", WiFi.localIP().toString().c_str());
  } else {
    Serial.println("\n❌ WiFi failed!");
  }
}

// ============================================================
// SETUP
// ============================================================
void setup() {
  Serial.begin(115200);
  Serial.printf("\n🚀 Smart Bin: %s\n", BIN_TYPE);
  
  // LED pins
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_LED_BLUE, OUTPUT);
  setLED("blink");
  
  // Servo PWM (ESP32 Core 3.x)
  initServo();
  
  // Weight sensor
  scale.begin(PIN_HX711_DT, PIN_HX711_SCK);
  calibrateScale();
  
  // WiFi
  setupWiFi();
  
  // MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  
  Serial.println("✅ Ready");
  setLED("standby");
}

// ============================================================
// LOOP
// ============================================================
void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();
  delay(10);
}
