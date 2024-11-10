import serial
from rplidar import RPLidar
import time

# Initialize connection with RPLidar and Arduino
lidar = RPLidar('COM16')
arduino = serial.Serial('COM22', 115200, timeout=1)

last_command = None
moving = False  # Biến cờ để theo dõi trạng thái di chuyển

def Send(command):
    global last_command
    if command != last_command:
        arduino.write(command.encode())
        last_command = command

def control_robot(angle, distance):
    global moving  # Sử dụng biến cờ
    
    # Initialize default command as stop
    command = 'T,254,254\n'  # Stop by default if no matching condition
    
    if distance < 500 and not moving:  # Kiểm tra khoảng cách và trạng thái di chuyển
        # Determine movement direction based on angle
        if angle <= 330 or angle >= 270:
            command = 'R,40,40,'  # Turn right
            moving = True
            
        elif 240 <= angle <= 300:
            command = 'L,40,40\n'  # Turn left
            moving = True
            
        elif angle <= 50 or angle >= 310:
            command = 'B,40,40\n'  # Move backward
            moving = True
            
        # Gửi lệnh và chờ một khoảng thời gian để tránh nhiễu
        Send(command)
        time.sleep(1)  # Chờ 1 giây trước khi gửi lệnh tiếp theo
        moving = False  # Đặt lại trạng thái sau khi di chuyển
        
    elif distance >= 500:  # Nếu không có vật cản, tiến thẳng
        command = 'S,40,40\n'  # Move straight forward
        Send(command)

try:
    for scan in lidar.iter_scans():
        for _, angle, distance in scan:
            control_robot(angle, distance)
finally:
    # Stop Lidar and disconnect
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    arduino.close()
