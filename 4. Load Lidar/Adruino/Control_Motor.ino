const int pwmPin = 6;   
const int startPin = 7; 
const int cwwPin = 5;   
const int pwmPin2 = 9;   
const int startPin2 = 10; 
const int cwwPin2 = 8;   

void trai(byte xungP, byte xungT){
  digitalWrite(startPin, HIGH); 
  digitalWrite(cwwPin,HIGH);     
  analogWrite(pwmPin,xungP);     
  digitalWrite(startPin2, HIGH); 
  digitalWrite(cwwPin2,HIGH);    
  analogWrite(pwmPin2,xungT);      
}
void phai(byte xungP, byte xungT){
  digitalWrite(startPin, HIGH); 
  digitalWrite(cwwPin,LOW);     
  analogWrite(pwmPin,xungP);   
  digitalWrite(startPin2, HIGH); 
  digitalWrite(cwwPin2,LOW);     
  analogWrite(pwmPin2,xungT);
}

void dilui(byte xungP, byte xungT){
  digitalWrite(startPin, HIGH); 
  digitalWrite(cwwPin,LOW);     
  digitalWrite(startPin2, HIGH); 
  digitalWrite(cwwPin2,HIGH);     
  analogWrite(pwmPin,xungP);      
  analogWrite(pwmPin2,xungT);      
}

void ditien(byte xungP, byte xungT){
  digitalWrite(startPin, HIGH); 
  digitalWrite(cwwPin,HIGH);     
  digitalWrite(startPin2, HIGH); 
  digitalWrite(cwwPin2,LOW);     
  analogWrite(pwmPin2,xungT);      
  analogWrite(pwmPin,xungP);      
}

void setup(){
  Serial.begin(9600);
  pinMode(pwmPin, OUTPUT);
  pinMode(startPin, OUTPUT);
  pinMode(cwwPin, OUTPUT);
  pinMode(pwmPin2, OUTPUT);
  pinMode(startPin2, OUTPUT);
  pinMode(cwwPin2, OUTPUT);
}
void loop(){
 //trai(100, 200);
 //Serial.println("Trái");
 //delay(5000);
 // Phải qua trái
 for(int i=0; i < 256; i++){
  phai(i,i);
  Serial.println(i);
  delay(50);
 }
 delay(5000);
 for(int i=255; i > -1; i--){
  phai(i,i);
  Serial.println(i);
  delay(50);
 }
 // Trái qua phải
 for(int i=0; i < 256; i++){
  trai(i,i);
  Serial.println(i);
  delay(50);
 }
 delay(5000);
 for(int i=255; i > -1; i--){
  trai(i,i);
  Serial.println(i);
  delay(50);
 }
 delay(5000);
 // Đi tiến
 for(int i=0; i < 256; i++){
  ditien(i,i);
  Serial.println(i);
  delay(50);
 }
 delay(5000);
 for(int i=255; i > -1; i--){
  ditien(i,i);
  Serial.println(i);
  delay(50);
 }
 delay(5000);
 // Đi lùi
 for(int i=0; i < 256; i++){
  dilui(i,i);
  Serial.println(i);
  delay(50);
 }
 delay(5000);
 for(int i=255; i > -1; i--){
  dilui(i,i);
  Serialpip.println(i);
  delay(50);
 }
 delay(5000);
}
