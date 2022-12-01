const int rightSensorPin = 7;
const int leftSensorPin = 6;
boolean rightVal = 0;
boolean leftVal = 0;

void setup()
{
  pinMode(leftSensorPin, INPUT); //Make pin 8 an input pin.
  pinMode(rightSensorPin, INPUT); //Make pin 7 an input pin.
  Serial.begin (9600); // initialize the serial port:
}
  
void loop ()
{
  //poll inputs for signal
  rightVal = digitalRead(rightSensorPin);
  leftVal = digitalRead(leftSensorPin);
  
  // when the sensor detects a signal above the threshold value set on sensor, turn finder to the direction of sound
  if (leftVal == LOW && rightVal == HIGH)
  {
    Serial.println("Turning Right");
    rightVal = 0;
    leftVal = 0;
  }
  else if (leftVal==HIGH && rightVal==LOW)
  {
    Serial.println("Turning Left");
    rightVal = 0;
    leftVal = 0;
  }
  else 
  {
    //Do nothing
    rightVal = 0;
    leftVal = 0;
  }
}