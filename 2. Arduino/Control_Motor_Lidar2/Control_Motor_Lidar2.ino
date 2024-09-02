#define pwmPin 6   
#define startPin 7 
#define cwwPin 5  
#define pwmPin2 9   
#define startPin2 10 
#define cwwPin2 8  

void Left(byte xungP, byte xungT){
  digitalWrite(startPin, HIGH); 
  digitalWrite(cwwPin,HIGH);          
  digitalWrite(startPin2, HIGH); 
  analogWrite(pwmPin,xungP);
  digitalWrite(cwwPin2,HIGH);
  analogWrite(pwmPin2,xungT);          
}
void Right(byte xungP, byte xungT){
  digitalWrite(startPin, HIGH); 
  digitalWrite(cwwPin,LOW);
  analogWrite(pwmPin,xungP);       
  digitalWrite(startPin2, HIGH); 
  digitalWrite(cwwPin2,LOW);
  analogWrite(pwmPin2,xungT);     
}

void Back(byte xungP, byte xungT){    
  digitalWrite(startPin, HIGH); 
  digitalWrite(cwwPin,LOW);
  analogWrite(pwmPin,xungP);       
  digitalWrite(startPin2, HIGH); 
  digitalWrite(cwwPin2,HIGH);
  analogWrite(pwmPin2,xungT);           
}

void Straight(byte xungP, byte xungT){
  analogWrite(pwmPin,xungP); 
  analogWrite(pwmPin2,xungT);        
  digitalWrite(startPin, HIGH); 
  digitalWrite(cwwPin,HIGH);  
  digitalWrite(startPin2, HIGH); 
  digitalWrite(cwwPin2,LOW);           
}

void Stop(){
  digitalWrite(startPin, LOW); 
  digitalWrite(cwwPin,LOW);    
  digitalWrite(startPin2, LOW); 
  digitalWrite(cwwPin2,LOW);        
}

void smoothControl(int currentP, int currentT, int targetP, int targetT) {
  int stepP = (targetP - currentP) / 10;
  int stepT = (targetT - currentT) / 10;

  for(int i = 0; i <= 10; i++) {
    analogWrite(pwmPin, currentP + stepP * i);
    analogWrite(pwmPin2, currentT + stepT * i);
    delay(10); // Delay ngắn để cập nhật mượt hơn
  }
}

void setup(){
  Serial.begin(115200);
  
  pinMode(pwmPin, OUTPUT);
  pinMode(startPin, OUTPUT);
  pinMode(cwwPin, OUTPUT);
  pinMode(pwmPin2, OUTPUT);
  pinMode(startPin2, OUTPUT);
  pinMode(cwwPin2, OUTPUT);
}

void loop(){
 if(Serial.available() > 0){
  String Read = Serial.readStringUntil('\n');
  Serial.println(Read);
  int pwmP = splitStr(Read, ",", 1).toInt();
  int pwmT = splitStr(Read, ",", 2).toInt();

  if(Read.startsWith("S")){
    smoothControl(analogRead(pwmPin), analogRead(pwmPin2), pwmP, pwmT);
    Straight(pwmP, pwmT);
  }

  if(Read.startsWith("B")){
    smoothControl(analogRead(pwmPin), analogRead(pwmPin2), pwmP, pwmT);
    Back(pwmP, pwmT);
  }

  if(Read.startsWith("R")){
    smoothControl(analogRead(pwmPin), analogRead(pwmPin2), pwmP, pwmT);
    Right(pwmP, pwmT);
  }

  if(Read.startsWith("L")){
    smoothControl(analogRead(pwmPin), analogRead(pwmPin2), pwmP, pwmT);
    Left(pwmP, pwmT);
  }

  if(Read.startsWith("T")){
    Stop();
  }
 }
}

String splitStr(String inputString, String delim, uint16_t pos){
  String tmp = inputString;
  for(int i=0; i<pos; i++){
    tmp = tmp.substring(tmp.indexOf(delim)+1);
    if(tmp.indexOf(delim)== -1 && i != pos -1)
      return "";
  }
  return tmp.substring(0,tmp.indexOf(delim));
}
