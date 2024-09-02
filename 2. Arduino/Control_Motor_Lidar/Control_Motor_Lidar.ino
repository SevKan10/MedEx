#define pwmPin1 6   
#define startPin1 7 
#define cwwPin1 5

#define pwmPin2 9   
#define startPin2 10 
#define cwwPin2 8  

#define rampStep 1  // Tốc độ thay đổi (mỗi bước tăng thêm bao nhiêu)
#define rampDelay 0  // Thời gian chờ giữa các bước (ms)

void setup() {
  Serial.begin(115200);

  pinMode(startPin1, OUTPUT);
  pinMode(cwwPin1, OUTPUT);
  pinMode(pwmPin1, OUTPUT);

  pinMode(startPin2, OUTPUT);
  pinMode(cwwPin2, OUTPUT);
  pinMode(pwmPin2, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    Serial.println(command);

    if (command.startsWith("S")) {
      goFoward(splitStr(command, ",", 1).toInt(), splitStr(command, ",", 2).toInt());
    } else if (command.startsWith("B")) {
      comeBack(splitStr(command, ",", 1).toInt(), splitStr(command, ",", 2).toInt());
    } else if (command.startsWith("R")) {
      turnRight(splitStr(command, ",", 1).toInt(), splitStr(command, ",", 2).toInt());
    } else if (command.startsWith("L")) {
      turnLeft(splitStr(command, ",", 1).toInt(), splitStr(command, ",", 2).toInt());
    } else if (command.startsWith("T")) {
      stopMove(254, 254);
    }
  }
}

String splitStr(String inputString, String delim, uint16_t pos) {
  String tmp = inputString;
  for (int i = 0; i < pos; i++) {
    tmp = tmp.substring(tmp.indexOf(delim) + 1);
    if (tmp.indexOf(delim) == -1 && i != pos - 1) 
      return "";
  }
  return tmp.substring(0, tmp.indexOf(delim));
}
