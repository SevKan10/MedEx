import serial

# Khởi tạo kết nối Arduino
def begin_COM():
    global arduino
    arduino = serial.Serial('COM20', 115200, timeout=1)

def Send(Data):
    arduino.write((Data + '\n').encode())

def reset():
    global speed
    speed = 0
    global speed_up 
    speed_up = 0
