#include <dht.h>

dht DHT;

#define DHT11_PIN 12

void setup(){
  Serial.begin(9600);
}

void loop()
{
  int chk = DHT.read11(DHT11_PIN);
  Serial.print("Temperature = ");
  Serial.print((int)round(1.8*DHT.temperature+32));
  Serial.println(" *F");
  Serial.print("Humidity = ");
  Serial.println(DHT.humidity);
  delay(1000);
}

