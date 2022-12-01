#include <SPI.h>
#include <SD.h>
File myFile;
int vib_sensor = A3; 
int vib_data = 0; 
int microphone = A0;
double seconds = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(vib_sensor, INPUT); 
  while (!Serial) {
    ;
  }
  Serial.print("Initializing SD Card...");

  if (!SD.begin(10)) {
    Serial.println("initialization failed!");
    while (1);
  }

  Serial.println("initialization done.");
}

void loop() {
  // put your main code here, to run repeatedly:
  vib_data = analogRead(vib_sensor); 
  if (vib_data >= 500) {
    myFile = SD.open("test.csv", FILE_WRITE);
    if (myFile) {
      Serial.println("Writing to test.csv...");
      myFile.print(analogRead(A0));
      myFile.print(",");
      myFile.print(seconds);
      myFile.println(",");
      myFile.close();
      Serial.print("Time elapsed (s): ");
      Serial.println(seconds);
    }
    seconds = seconds + 0.5;
    delay(500);
  }
  else {
    myFile = SD.open("test.csv", FILE_WRITE);
    if (myFile) {
      Serial.println("No voice detected");
      myFile.print("0");
      myFile.print(",");
      myFile.print(seconds);
      myFile.println(",");
      myFile.close();
      Serial.print("Time elapsed (s): ");
      Serial.println(seconds);
    }
    seconds = seconds + 0.5;
    delay(500);
  }
}