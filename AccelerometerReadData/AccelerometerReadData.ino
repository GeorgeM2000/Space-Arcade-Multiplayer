#include <Arduino_LSM9DS1.h>

bool commandRecv = false;
bool startStream = false;


void setup() {
  Serial.begin(115200);
  while(!Serial);

  if(!IMU.begin()){
    Serial.println("Failed to initalize IMU");
    while(1);
  }

  Serial.println("To start collecting data enter 's'.");
  Serial.println("To end collecting data enter 'e'.");
}

void loop() {
  String command;
  
  while(Serial.available()){
    char c = Serial.read();
    if ((c != '\n') && (c != '\r')) {
      command.concat(c);
    } 
    else if (c == '\r') {
      commandRecv = true;
      command.toLowerCase();
    }
  }


  if(commandRecv) {
    commandRecv = false;
    if(command == "s"){
      if(!startStream) startStream = true;
    }
    else if(command == "e") {
      if(startStream) startStream = false;
    }
  }
  
  float x, y, z;
  if (startStream) {
     // testing accelerometer
     if (IMU.accelerationAvailable()) {
        IMU.readAcceleration(x, y, z);
  
        Serial.println(y);
        delay(50);
        
      }
  }
  
}
