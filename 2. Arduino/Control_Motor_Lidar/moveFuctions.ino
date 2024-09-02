void turnLeft(byte pwmR, byte pwmL) {
  for (int i = 0; i <= pwmR; i += rampStep) {
    digitalWrite(startPin1, 1); 
    digitalWrite(cwwPin1, 1);          
    analogWrite(pwmPin1, i);
    delay(rampDelay);
  }

  for (int i = 0; i <= pwmL; i += rampStep) {
    digitalWrite(startPin2, 1); 
    digitalWrite(cwwPin2, 1);
    analogWrite(pwmPin2, i);          
    delay(rampDelay);
  }
}

void turnRight(byte pwmR, byte pwmL) {
  for (int i = 0; i <= pwmR; i += rampStep) {
    digitalWrite(startPin1, 1); 
    digitalWrite(cwwPin1, 0);
    analogWrite(pwmPin1, i);       
    delay(rampDelay);
  }

  for (int i = 0; i <= pwmL; i += rampStep) {
    digitalWrite(startPin2, 1); 
    digitalWrite(cwwPin2, 0);
    analogWrite(pwmPin2, i);    
    delay(rampDelay);
  }
}

void comeBack(byte pwmR, byte pwmL) {
  for (int i = 0; i <= pwmR; i += rampStep) {
    digitalWrite(startPin1, 1); 
    digitalWrite(cwwPin1, 0);
    analogWrite(pwmPin1, i);      
    delay(rampDelay);
  }

  for (int i = 0; i <= pwmL; i += rampStep) {
    digitalWrite(startPin2, 1); 
    digitalWrite(cwwPin2, 1);
    analogWrite(pwmPin2, i);           
    delay(rampDelay);
  }
}

void goFoward(byte pwmR, byte pwmL) {
  for (int i = 0; i <= pwmR; i += rampStep) {
    digitalWrite(startPin1, 1); 
    digitalWrite(cwwPin1, 1);  
    analogWrite(pwmPin1, i);
    delay(rampDelay);
  }

  for (int i = 0; i <= pwmL; i += rampStep) {
    digitalWrite(startPin2, 1); 
    digitalWrite(cwwPin2, 0); 
    analogWrite(pwmPin2, i);        
    delay(rampDelay);
  }
}

void stopMove(byte pwmR, byte pwmL) {
  // Giảm tốc từ từ
  for (int i = pwmR; i >= 250; i += rampStep) {
    digitalWrite(startPin1, 0); 
    digitalWrite(cwwPin1, 0);    
    analogWrite(pwmPin1, i);
    delay(rampDelay);
  }

  for (int i = pwmL; i >= 250; i += rampStep) {
    digitalWrite(startPin2, 0); 
    digitalWrite(cwwPin2, 0);        
    analogWrite(pwmPin2, i);        
    delay(rampDelay);
  }
}