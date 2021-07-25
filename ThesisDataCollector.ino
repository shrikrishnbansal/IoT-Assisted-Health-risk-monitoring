#include "MAX30100_PulseOximeter.h"
#include <Wire.h>
#include <ArduinoBLE.h>
#include <ArduinoJson.h>
#include "DHT.h"

BLEService healthRiskService("1101");
BLEUnsignedCharCharacteristic healthRiskChar("1101", BLERead | BLENotify);

#define REPORTING_PERIOD_MS     1000
PulseOximeter pox;
uint32_t tsLastReport = 0;
#define DHTPIN 2     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11
DHT dht(DHTPIN, DHTTYPE);
int val;
int tempPin = 1;
char sbuffer[30], ch;
unsigned char pos;
unsigned char sbp, dbp;
int age = 20;
int gender = 1;
int hs;

//void onBeatDetected()
//{
//    Serial.println("Beat!");
//}

void setup() {
  Serial.begin(9600);
  dht.begin();

  if (!BLE.begin()) 
  {
    Serial.println("starting BLE failed!");
    while (1);
  }
  
  BLE.setLocalName("HealthRisk");
  BLE.setAdvertisedService(healthRiskService);
  healthRiskService.addCharacteristic(healthRiskChar);
  BLE.addService(healthRiskService);
  
  BLE.advertise();
  Serial.println("Bluetooth device active, waiting for connections...");
  
  if (!pox.begin()) {
        Serial.println("FAILED");
        for(;;);
    } else {
        Serial.println("SUCCESS");
    }
     pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
 
    //pox.setOnBeatDetectedCallback(onBeatDetected);
}

char mygetchar(void)
{ //receive serial character from sensor (blocking while nothing received)
 while (!Serial.available());
 return Serial.read();
}

void loop() {
  delay(2000);
  BLEDevice central = BLE.central();
  ch = mygetchar(); //loop till character received
 if(ch==0x0A) // if received character is , 0x0A, 10 then process buffer
 {
     pos = 0; // buffer position reset for next reading

     // extract data from serial buffer to 8 bit integer value
     // convert data from ASCII to decimal
     sbp = ((sbuffer[1]-'0')*100) + ((sbuffer[2]-'0')*10) +(sbuffer[3]-'0');
     dbp = ((sbuffer[6]-'0')*100) + ((sbuffer[7]-'0')*10) +(sbuffer[8]-'0');
     
 } else { //store serial data to buffer
     sbuffer[pos] = ch;
     pos++;
 }
  
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  int st = (int)t;
  val = analogRead(tempPin);
  float mv = val * (3300 / 1024.0);
  float bt = mv/10;
   pox.update();
   int hr, spo2;
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
      hr = pox.getHeartRate();
      spo2 = pox.getSpO2();
       tsLastReport = millis();
    }

  if (central) 
  {
    Serial.print("Connected to central: ");
    Serial.println(central.address());    
    while (central.connected()) {
          DynamicJsonBuffer jsonBuffer;
          String input =
              "{\"age\":age,\"gender\":gender,\"HR\":HR,\"SBP\":SBP,\"DBP\":DBP,\"st\":st,\"bt\":bt,\"spo2\":spo2,}";
          JsonObject& root = jsonBuffer.parseObject(input);
          root.printTo(Serial);
          Serial.println();
          //healthRiskChar.writeValue(root);
          delay(200);
    }
  }
}
