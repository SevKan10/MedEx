import serial
import time
from rplidar import RPLidar

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

# Khởi tạo kết nối với RPLidar
lidar = RPLidar('COM16')

# Hàm điều khiển robot dựa trên góc và khoảng cách
def control_robot(angle, distance):
    # Nếu khoảng cách nhỏ hơn 500 mm thì di chuyển
    if distance < 500:
        if angle >= 60 and angle <= 110:
            Send(f"L,{int(10)},{int(10)},")  # Move left
            time.sleep(1)  # Robot sẽ di chuyển trong 1 giây
        elif angle >= 210 and angle <= 300:
            Send(f"R,{int(10)},{int(10)},")  # Move right
            time.sleep(1)  # Robot sẽ di chuyển trong 1 giây
        elif angle <= 50 or angle >= 310:
            Send(f"B,{int(10)},{int(10)},")  # Move backward
            time.sleep(1)  # Robot sẽ di chuyển trong 1 giây
    else:
        Send(f"S,{int(10)},{int(10)},")  # Stop

try:
    begin_COM()
    for scan in lidar.iter_scans():
        for _, angle, distance in scan:
            control_robot(angle, distance)
            break  # Stop scanning once a movement is issued
        time.sleep(2)  # Pause before the next scan cycle
finally:
    # Dừng Lidar và ngắt kết nối
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    arduino.close()
