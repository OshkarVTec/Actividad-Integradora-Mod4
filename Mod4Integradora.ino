//Este programa lee la entrada de 4 push buttons y la transmite por el puerto serial
  
  int pinBtn1 = 3; //w
  int pinBtn2 = 4; //a
  int pinBtn3 = 5; //s
  int pinBtn4 = 6; //d

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);//Iniciamos la comunicación serial
  pinMode(pinBtn1, INPUT_PULLUP);
  pinMode(pinBtn2, INPUT_PULLUP);
  pinMode(pinBtn3, INPUT_PULLUP);
  pinMode(pinBtn4, INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(digitalRead(pinBtn1)==0){
    Serial.println("w");
    delay(300);
  }
  if(digitalRead(pinBtn2)==0){
    Serial.println("a");
    delay(300);
  }
  if(digitalRead(pinBtn3)==0){
    Serial.println("s");
    delay(300);
  }
  if(digitalRead(pinBtn4)==0){
    Serial.println("d");
    delay(300);
  }
}
