int vib_sensor = A3; 
int vib_data = 0; 

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
pinMode(vib_sensor, INPUT); 

}

void loop() {
  // put your main code here, to run repeatedly:
vib_data = analogRead(vib_sensor); 
Serial.println(vib_data);
delay(100);
}