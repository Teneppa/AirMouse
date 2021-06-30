/*
  This is a really buggy demo. Use it at your own risk.
  
  - Teemu
*/

/* =========================== WiFi =============================== */
#include <ESP8266WiFi.h>

// PUT YOUR WIFI PASSWORD AND NAME (SSID) HERE!
#ifndef STASSID
#define STASSID ""
#define STAPSK  ""
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

WiFiServer wifiServer(8421);

/* ======================== STATIC IP ============================= */
IPAddress staticIP(10, 0, 0, 184);
IPAddress gateway(10, 0, 0, 1);
IPAddress subnet(255, 255, 255, 0);
IPAddress dns(1, 1, 1, 1);

/* =========================== BNO ================================ */

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

bool buttonStatus = true;
Adafruit_BNO055 bno = Adafruit_BNO055(55, 0x29);

/* ========================== SETUP =============================== */

void setup() {
  Serial.begin(115200);

  pinMode(D4, INPUT_PULLUP);

  /* Initialise the sensor */
  if (!bno.begin()) {
    Serial.println("CAN'T INITIALIZE");
    while (1);
  }

  delay(1000);

  /* WIFI */
  WiFi.mode(WIFI_STA);

  //String newHostname = "AirMouse";

  //WiFi.hostname(newHostname.c_str());
  WiFi.config(staticIP, gateway, subnet, dns);

  WiFi.begin(ssid, password);
  while (WiFi.waitForConnectResult() != WL_CONNECTED) {
    Serial.println("Connection Failed! Rebooting...");
    delay(5000);
    ESP.restart();
  }

  Serial.println("Ready");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Last reset: "+ESP.getResetReason());

  wifiServer.begin();
}

char mg;
void loop() {
  WiFiClient client = wifiServer.available();

  if (client) {
    if (client.connected()) {
      Serial.println("Client Connected");
    }

    while (client.connected()) {

      while (client.available() > 0) {

        // read data from the connected client
        mg = client.read();
        client.flush();
        if (mg == 'd') {
          sensors_event_t orientationData;
          bno.getEvent(&orientationData, Adafruit_BNO055::VECTOR_EULER);
          sendBNOClient(&orientationData, &client);
        }

      }

    }
    client.stop();
    Serial.println("Client disconnected");
  }
}

char str[30];
void sendBNOClient(sensors_event_t * event, WiFiClient * wclient) {
  
  double x = -1000000, y = -1000000 , z = -1000000; //dumb values, easy to spot problem
  
  if (event->type == SENSOR_TYPE_ORIENTATION) {
    x = event->orientation.x;
    y = event->orientation.y;
    z = event->orientation.z;
  }

  buttonStatus = digitalRead(D4);

  strlcpy(str, String(String(x)+","+String(y)+","+String(z)+","+String(buttonStatus)).c_str(), 30);
  
  wclient -> println(str);
  wclient -> flush();
}
