#include <SPI.h>
#include <SD.h>
File myFile;
void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
  ; // wait for serial port to connect. Needed for native USB port only
  }
  Serial.print("Initializing SD card...");
  if (!SD.begin(10)) {
    Serial.println("initialization failed!");
    while (1);
  }

  Serial.println("initialization done.");
  
}

void loop() {
// open the file. note that only one file can be open at a time,
  // so you have to close this one before opening another.
  myFile = SD.open("test.csv", FILE_WRITE);
  // if the file opened okay, write to it:
  
  if (myFile) {
    Serial.print("Writing to test.txt...");
    myFile.print(analogRead(A0));
    myFile.println(",");
    // close the file:
    myFile.close();
    Serial.println("done.");
  } 
  else {
  // if the file didn't open, print an error:
    Serial.println("error opening test.txt");
  }
}