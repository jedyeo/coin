void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

int count = 0;
const double threshold = 3.3;


void loop() {
   int sensorValue = analogRead(A0);
   float voltage = sensorValue * (5.0/1023.0);
   Serial.println(voltage);

 /* if(voltage > threshold)
    digitalWrite(13, HIGH);
  else
    digitalWrite(13, LOW);*/
    //while(1);
    
  //  count++;
  // Serial.println(count);
    delay(1000);
}
