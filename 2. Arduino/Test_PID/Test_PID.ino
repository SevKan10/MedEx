#include <PID_v2.h>

// Định nghĩa các chân
#define pwmPin1 6   
#define startPin1 7 
#define cwwPin1 5

#define pwmPin2 9   
#define startPin2 10 
#define cwwPin2 8  

#define rampStep 5  // Tốc độ thay đổi 
#define rampDelay 10  // Thời gian chờ giữa các bước (ms)

// Tham số PID
double kp = 1, ki = 20, kd = 0;  // Điều chỉnh để đạt hiệu suất tốt nhất
double inputL = 0, outputL = 0, setpointL = 0;
double inputR = 0, outputR = 0, setpointR = 0;

// Tạo đối tượng PID cho hai động cơ
PID pidLeft(&inputL, &outputL, &setpointL, kp, ki, kd, DIRECT);
PID pidRight(&inputR, &outputR, &setpointR, kp, ki, kd, DIRECT);

void setup() {
  Serial.begin(115200);

  // Khởi tạo chân
  pinMode(startPin1, OUTPUT);
  pinMode(cwwPin1, OUTPUT);
  pinMode(pwmPin1, OUTPUT);

  pinMode(startPin2, OUTPUT);
  pinMode(cwwPin2, OUTPUT);
  pinMode(pwmPin2, OUTPUT);

  // Thiết lập PID
  pidLeft.SetMode(AUTOMATIC);
  pidLeft.SetOutputLimits(-255, 255);
  pidRight.SetMode(AUTOMATIC);
  pidRight.SetOutputLimits(-255, 255);
  
  // Khởi tạo giá trị đầu vào PID
  inputL = 0;
  inputR = 0;
  setpointL = 0;
  setpointR = 0;
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    Serial.println(command);

    if (command.startsWith("S")) {
      setpointL = splitStr(command, ",", 1).toInt();
      setpointR = splitStr(command, ",", 2).toInt();
      goFoward(setpointL, setpointR);
      
    } else if (command.startsWith("B")) {
      setpointL = splitStr(command, ",", 1).toInt();
      setpointR = splitStr(command, ",", 2).toInt();
      comeBack(setpointL, setpointR);

    } else if (command.startsWith("R")) {
      setpointL = splitStr(command, ",", 1).toInt();
      setpointR = splitStr(command, ",", 2).toInt();
      turnRight(setpointL, setpointR);

    } else if (command.startsWith("L")) {
      setpointL = splitStr(command, ",", 1).toInt();
      setpointR = splitStr(command, ",", 2).toInt();
      turnLeft(setpointL, setpointR);

    } else if (command.startsWith("T")) {
      stopMove(0, 0); // Dừng hẳn động cơ
    }
  }

  // Tính toán PID cho cả hai động cơ
  pidLeft.Compute();
  pidRight.Compute();

  // Gọi hàm điều khiển động cơ với giá trị đầu ra từ PID
  pwmOut(outputL, outputR);
}


// Hàm điều khiển động cơ
void pwmOut(int outL, int outR) {
  if (outL > 0) {
    digitalWrite(startPin1, HIGH);
    digitalWrite(cwwPin1, HIGH);
    analogWrite(pwmPin1, outL);
  } else {
    digitalWrite(startPin1, HIGH);
    digitalWrite(cwwPin1, LOW);
    analogWrite(pwmPin1, -outL);
  }

  if (outR > 0) {
    digitalWrite(startPin2, HIGH);
    digitalWrite(cwwPin2, HIGH);
    analogWrite(pwmPin2, outR);
  } else {
    digitalWrite(startPin2, HIGH);
    digitalWrite(cwwPin2, LOW);
    analogWrite(pwmPin2, -outR);
  }
}

// Hàm di chuyển thẳng
void goFoward(int pwmL, int pwmR) {
  setpointL = pwmL;
  setpointR = pwmR;
}

// Hàm quay ngược lại
void comeBack(int pwmL, int pwmR) {
  setpointL = -pwmL;
  setpointR = -pwmR;
}

// Hàm rẽ phải
void turnRight(int pwmL, int pwmR) {
  setpointL = pwmL;
  setpointR = -pwmR;
}

// Hàm rẽ trái
void turnLeft(int pwmL, int pwmR) {
  setpointL = -pwmL;
  setpointR = pwmR;
}

// Hàm dừng
void stopMove(int pwmL, int pwmR) {
  setpointL = 0;
  setpointR = 0;
}

// Hàm tách chuỗi
String splitStr(String inputString, String delim, uint16_t pos) {
  String tmp = inputString;
  for (int i = 0; i < pos; i++) {
    tmp = tmp.substring(tmp.indexOf(delim) + 1);
    if (tmp.indexOf(delim) == -1 && i != pos - 1) 
      return "";
  }
  return tmp.substring(0, tmp.indexOf(delim));
}
