const int greenPin = 6;
const int bluePin = 3;
const int redPin = 5;

void setup() {
  Serial.begin(9600);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(redPin, OUTPUT);
}

int redflag = 0;
int greenflag = 0;
int blueflag= 0;
char choice;

void loop() {
  choice = Serial.read();
  if(choice == 'r'){
    redflag = 1;
    blueflag = 0;
    greenflag = 0;
  }
  else if(choice=='g') {
    greenflag = 1;
    redflag = 0;
    blueflag = 0;
  }
  else if(choice=='b') {
    blueflag = 1;
    greenflag = 0;
    redflag = 0;
  }

  if (redflag){
    analogWrite(redPin, 255);
    analogWrite(bluePin, 0);
    analogWrite(greenPin, 0);
  }

  if (greenflag){
    analogWrite(redPin,0);
    analogWrite(bluePin, 0);
    analogWrite(greenPin, 255);
  }

  if (blueflag){
    analogWrite(redPin,0);
    analogWrite(bluePin, 255);
    analogWrite(greenPin, 0);
  }

  if(!redflag && !blueflag && !greenflag){
    analogWrite(redPin,0);
    analogWrite(bluePin, 0);
    analogWrite(greenPin, 0);
  }

    
}
