#include <LiquidCrystal.h>
LiquidCrystal lcd(8,9,5,4,3,2);
 
int pinSignal = A0; // pin connected to pin O module sound sensor  
int adc;

int db;
int PdB; //the variable that will hold the value read from the microphone each time
 
void setup ()  
{   
  Serial.begin(9600);
  pinMode (pinSignal, INPUT); // Set the signal pin as input   
  lcd.begin(16,2); 
}  
   
void loop ()  
{  
  adc = analogRead(A0); //Read the ADC value from amplifer
  db = (adc + 43.2073) / 3.003; //Convert ADC value to dB using Regression values
  PdB = db; //Store the previous of dB here
  lcd.setCursor(0, 0);
  lcd.print("Loudness: ");
  lcd.setCursor(0, 1);
  lcd.print(db);
  lcd.print("dB");

  if (PdB != db) {
    Serial.println(db);
  }

  if (db <= 60)
  {
    lcd.setCursor(0, 0);
    lcd.print("Level: Quiet");
  }
  else if (db > 60 && db < 85)
  {
    lcd.setCursor(0, 0);
    lcd.print("Level: Moderate");
  }
  else if (db >= 85)
  {
    lcd.setCursor(0, 0);
    lcd.print("Level: High");
  }
   
   delay(10); 
   lcd.clear();
}