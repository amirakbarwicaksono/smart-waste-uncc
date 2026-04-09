// ============================================================
// Smart Waste Bin - ESP32 Code (Slave Mode)
// Bin Type: RECYCLING
// ============================================================

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <HX711.h>

// ============================================================
// BIN CONFIGURATION
// ============================================================
#define BIN_TYPE "recycling"

const char* ssid = "Firas";
const char* password = "11111111";

const char* mqtt_server = "10.81.235.53";
const int mqtt_port = 1883;

const char* mqtt_topic_bin = "smart_waste/bin";
const char* mqtt_topic_weight = "smartwaste/user/weight";

// Pin Definitions
#define PIN_SERVO     13
#define PIN_HX711_DT  4
#define PIN_HX711_SCK 5
#define PIN_LED_RED   14
#define PIN_LED_GREEN 12
#define PIN_LED_BLUE  27

// Servo PWM Parameters
#define SERVO_FREQ    50
#define SERVO_RES     12
#define SERVO_MIN_US  500
#define SERVO_MAX_US  2500
#define US_TO_DUTY(us) (((us) * (1 << SERVO_RES)) / 20000)

// Weight Sensor Parameters
#define WEIGHT_THRESHOLD 50
#define WEIGHT_SAMPLE_COUNT 5

// Timing Parameters
#define USER_PLACEMENT_TIME 10000   // 10 seconds
#define MONITORING_TIME 20000       // 20 seconds

// ============================================================
// GLOBAL VARIABLES
// ============================================================
WiFiClient espClient;
PubSubClient client(espClient);
HX711 scale;

bool isOpen = false;
bool isProcessing = false;
String currentWasteType = "";
String currentUserId = "";
String currentTransactionId = "";

// State machine
enum BinState {
  BIN_IDLE,
  BIN_WAITING_USER,
  BIN_MONITORING,
};

BinState currentState = BIN_IDLE;
unsigned long stateStartTime = 0;
float maxWeight = 0;
unsigned long lastWeightCheck = 0;
unsigned long lastStatusPrint = 0;
bool phase1Completed = false;
int lastPrintedSecond = -1;

// ============================================================
// LED CONTROL
// ============================================================
void setLED(String status) {
  if (status == "standby") {
    digitalWrite(PIN_LED_RED, LOW);
    digitalWrite(PIN_LED_GREEN, HIGH);
    digitalWrite(PIN_LED_BLUE, LOW);
    Serial.println("LED: Standby (Green)");
  } 
  else if (status == "active") {
    digitalWrite(PIN_LED_RED, LOW);
    digitalWrite(PIN_LED_GREEN, LOW);
    digitalWrite(PIN_LED_BLUE, HIGH);
    Serial.println("LED: Active (Blue)");
  } 
  else if (status == "error") {
    digitalWrite(PIN_LED_RED, HIGH);
    digitalWrite(PIN_LED_GREEN, LOW);
    digitalWrite(PIN_LED_BLUE, LOW);
    Serial.println("LED: Error (Red)");
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
// SERVO CONTROL
// ============================================================
void initServo() {
  ledcAttach(PIN_SERVO, SERVO_FREQ, SERVO_RES);
  int duty = US_TO_DUTY(SERVO_MIN_US);
  ledcWrite(PIN_SERVO, duty);
  Serial.println("Servo initialized (closed position)");
}

void setServoAngle(int angle) {
  if (angle < 0) angle = 0;
  if (angle > 180) angle = 180;
  int pulseWidth = SERVO_MIN_US + (angle * (SERVO_MAX_US - SERVO_MIN_US) / 180);
  int duty = US_TO_DUTY(pulseWidth);
  ledcWrite(PIN_SERVO, duty);
}

void openBin() {
  if (!isOpen) {
    Serial.println("Opening bin...");
    setServoAngle(180);
    isOpen = true;
    setLED("active");
  }
}

void closeBin() {
  if (isOpen) {
    Serial.println("Closing bin...");
    setServoAngle(0);
    isOpen = false;
    setLED("standby");
  }
}

// ============================================================
// WEIGHT SENSOR
// ============================================================
void calibrateScale() {
  Serial.println("Calibrating scale...");
  Serial.println("Make sure no weight on the scale");
  delay(3000);
  scale.tare();
  Serial.println("Scale tared");
}

float readWeight() {
  if (scale.is_ready()) {
    float weight = scale.get_units(WEIGHT_SAMPLE_COUNT);
    if (weight < 0) weight = 0;
    return weight;
  }
  return 0;
}

// ============================================================
// SEND FINAL WEIGHT REPORT - SESUAI SPESIFIKASI
// ============================================================
void sendFinalWeightReport() {
  bool weightDetected = (maxWeight > WEIGHT_THRESHOLD);
  
  // Hanya field yang sesuai spesifikasi
  JsonDocument doc;
  doc["weight_status"] = weightDetected;
  doc["waste_type"] = currentWasteType;
  doc["bin_type"] = BIN_TYPE;
  doc["user_id"] = currentUserId;
  
  String output;
  serializeJson(doc, output);
  
  // Pastikan MQTT connected
  if (!client.connected()) {
    Serial.println("MQTT not connected, reconnecting...");
    reconnectMQTT();
  }
  
  // Kirim dengan retry
  bool sent = false;
  for (int attempt = 0; attempt < 3; attempt++) {
    if (client.publish(mqtt_topic_weight, output.c_str())) {
      Serial.printf("Weight report sent: %s\n", output.c_str());
      sent = true;
      break;
    }
    delay(100);
    client.loop();
  }
  
  if (!sent) {
    Serial.println("Failed to send weight report!");
  }
}

// ============================================================
// START BIN OPERATION
// ============================================================
void startBinOperation() {
  Serial.println("Starting bin operation (30 second monitoring)...");
  openBin();
  
  maxWeight = 0;
  lastWeightCheck = 0;
  lastStatusPrint = 0;
  lastPrintedSecond = -1;
  phase1Completed = false;
  
  currentState = BIN_WAITING_USER;
  stateStartTime = millis();
  
  Serial.printf("Phase 1: User has %d seconds to place waste\n", USER_PLACEMENT_TIME / 1000);
}

// ============================================================
// PROCESS BIN OPERATION
// ============================================================
void processBinOperation() {
  if (currentState == BIN_IDLE) return;
  
  unsigned long now = millis();
  unsigned long elapsed = now - stateStartTime;
  
  // KRITICAL: Keep MQTT alive during entire operation
  client.loop();
  
  switch(currentState) {
    case BIN_WAITING_USER:
      if (elapsed >= USER_PLACEMENT_TIME) {
        if (!phase1Completed) {
          phase1Completed = true;
          Serial.println("Phase 2: Monitoring weight for 20 seconds");
          currentState = BIN_MONITORING;
          stateStartTime = now;
          lastWeightCheck = 0;
        }
      } else {
        int currentSecond = (USER_PLACEMENT_TIME - elapsed) / 1000;
        if (currentSecond != lastPrintedSecond && currentSecond >= 0 && currentSecond <= 10) {
          lastPrintedSecond = currentSecond;
          if (currentSecond > 0) {
            Serial.printf("  Place waste in: %d seconds\n", currentSecond);
          }
        }
      }
      break;
      
    case BIN_MONITORING:
      // Check weight every 500ms
      if (now - lastWeightCheck >= 500) {
        lastWeightCheck = now;
        float currentWeight = readWeight();
        if (currentWeight > maxWeight) {
          maxWeight = currentWeight;
        }
      }
      
      // Print status every 2 seconds (reduce serial noise)
      if (now - lastStatusPrint >= 2000) {
        lastStatusPrint = now;
        float elapsedSec = elapsed / 1000.0;
        Serial.printf("  Monitoring: %.1f sec, Max weight: %.2f g\n", elapsedSec, maxWeight);
      }
      
      if (elapsed >= MONITORING_TIME) {
        Serial.println("Monitoring complete, sending final report...");
        sendFinalWeightReport();
        closeBin();
        
        Serial.printf("Bin operation complete. Max weight: %.2f g, Detection: %s\n", 
                      maxWeight, (maxWeight > WEIGHT_THRESHOLD) ? "YES" : "NO");
        
        isProcessing = false;
        currentWasteType = "";
        currentUserId = "";
        currentTransactionId = "";
        currentState = BIN_IDLE;
      }
      break;
      
    default:
      break;
  }
}

// ============================================================
// MQTT CALLBACK
// ============================================================
void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.printf("MQTT Received [%s]: %s\n", topic, message.c_str());
  
  if (strcmp(topic, mqtt_topic_bin) != 0) return;
  
  JsonDocument doc;
  DeserializationError error = deserializeJson(doc, message);
  
  if (error) {
    Serial.printf("JSON parsing error: %s\n", error.c_str());
    return;
  }
  
  String targetBin = doc["bin_type"] | "";
  if (targetBin != BIN_TYPE) {
    Serial.printf("Command not for this bin (target: %s, my: %s)\n", targetBin.c_str(), BIN_TYPE);
    return;
  }
  
  String state = doc["state"] | "";
  
  if (state == "open") {
    if (isProcessing || currentState != BIN_IDLE) {
      Serial.println("Busy, ignoring open command");
      return;
    }
    
    currentUserId = doc["barcode"] | "";
    currentWasteType = doc["waste_type"] | "unknown";
    currentTransactionId = doc["transaction_id"] | "";
    
    Serial.printf("Open command received - User: %s, Waste: %s\n", 
                  currentUserId.c_str(), currentWasteType.c_str());
    
    isProcessing = true;
    startBinOperation();
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
      Serial.println("Connected");
      client.subscribe(mqtt_topic_bin);
      Serial.printf("Subscribed to: %s\n", mqtt_topic_bin);
      setLED("standby");
    } else {
      Serial.print("Failed, rc=");
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
    Serial.printf("\nWiFi connected, IP: %s\n", WiFi.localIP().toString().c_str());
  } else {
    Serial.println("\nWiFi connection failed!");
  }
}

// ============================================================
// SETUP
// ============================================================
void setup() {
  Serial.begin(115200);
  Serial.printf("\nSmart Bin: %s\n", BIN_TYPE);
  Serial.println("==========================================");
  
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_LED_BLUE, OUTPUT);
  setLED("blink");
  
  initServo();
  
  scale.begin(PIN_HX711_DT, PIN_HX711_SCK);
  calibrateScale();
  
  setupWiFi();
  
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  
  Serial.println("System Ready");
  Serial.println("==========================================");
  setLED("standby");
}

// ============================================================
// MAIN LOOP
// ============================================================
void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  
  client.loop();  // This must run frequently!
  processBinOperation();
  
  delay(10);
}