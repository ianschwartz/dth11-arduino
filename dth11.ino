#include <ArduinoJson.h>
#include <dht.h>

dht DHT;

#define DHT11_PIN 7

void setup(){
  Serial.begin(19200);
}

void loop()
{
  int chk = DHT.read11(DHT11_PIN);
//  String reading = "{ 'temp': " + String((int)round(DHT.temperature)) + ", 'humidity': " + String(DHT.humidity) + " }";
//  Serial.println(reading);
  delay(1000);

  //
// Step 1: Reserve memory space
//
  StaticJsonBuffer<200> jsonBuffer;

//
// Step 2: Build object tree in memory
//
  JsonObject& root = jsonBuffer.createObject();
  root["temp"] = (int)round(DHT.temperature);
  root["humidity"] = DHT.humidity;

//
// Step 3: Generate the JSON string
//
root.printTo(Serial);
Serial.println("");
}

