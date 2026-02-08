#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Configuration WiFi
const char* ssid = "IPhone";
const char* password = "yanishasni";

// Configuration MQTT
const char* mqtt_server = "raspberrypi.local";
const char* mqtt_topic = "  ";
const int ledPin = 12;      // Pin pour la LED
const int buttonPin = 14;   // Pin pour le bouton poussoir

WiFiClient espClient;
PubSubClient client(espClient);
bool ledState = false;  // État actuel de la LED

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connexion à ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connecté");
  Serial.println("Adresse IP : ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  // Conversion du message en string
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.print("Message reçu : ");
  Serial.println(message);

  if (message == "on") {
    digitalWrite(ledPin, HIGH);
    ledState = true;
  } else if (message == "off") {
    digitalWrite(ledPin, LOW);
    ledState = false;
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Connexion au serveur MQTT...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connecté");
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("Échec, rc=");
      Serial.print(client.state());
      Serial.println(" nouvelle tentative dans 5 secondes");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);  // Utilise la résistance pull-up interne
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  // Vérifier si le bouton est pressé
  if (digitalRead(buttonPin) == LOW) {
    delay(50); // anti-rebond
    if (ledState) {
      client.publish(mqtt_topic, "off");
    } else {
      client.publish(mqtt_topic, "on");
    }
    delay(500);  // évite les actions répétées
  }
}