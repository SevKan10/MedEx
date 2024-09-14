import time
import serial
from rplidar import RPLidar

# Định nghĩa các giá trị cần thiết
MIN_DISTANCE = 300  # Khoảng cách tối thiểu (30 cm)
SERIAL_PORT = '/dev/ttyUSB0'  # Thay đổi cổng USB tùy theo thiết bị LIDAR
ARDUINO_PORT = '/dev/ttyACM0'  # Cổng USB Arduino, thay đổi tùy thiết bị
BAUD_RATE = 115200  # Baudrate cần khớp với Arduino

# Khởi tạo kết nối với LIDAR và Arduino
lidar = RPLidar(SERIAL_PORT)
arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Đợi Arduino khởi động

# Hàm gửi tín hiệu điều khiển đến Arduino
def send_to_arduino(command):
    arduino.write(f"{command}\n".encode())
    print(f"Sent to Arduino: {command}")

# Hàm để xử lý dữ liệu từ LIDAR và gửi tín hiệu điều khiển đến Arduino
def process_data(data):
    left_distance = None
    right_distance = None

    for scan in data:
        angle = int(scan[1])
        distance = float(scan[2])

        if angle > 315 or angle < 45:  # Vùng trước bên phải
            if right_distance is None or distance < right_distance:
                right_distance = distance
        elif angle > 135 and angle < 225:  # Vùng trước bên trái
            if left_distance is None or distance < left_distance:
                left_distance = distance

    # Kiểm tra và điều khiển động cơ
    if left_distance is not None and left_distance < MIN_DISTANCE:
        # Rẽ phải
        print("Turning right")
        send_to_arduino("R,200,200")
    elif right_distance is not None and right_distance < MIN_DISTANCE:
        # Rẽ trái
        print("Turning left")
        send_to_arduino("L,200,200")
    elif left_distance is not None and right_distance is not None and left_distance < MIN_DISTANCE and right_distance < MIN_DISTANCE:
        # Cả hai bên có vật cản, đi thẳng
        print("Obstacle on both sides, going straight")
        send_to_arduino("S,200,200")
    else:
        # Đi thẳng
        print("Going straight")
        send_to_arduino("S,200,200")

# Chương trình chính
if __name__ == '__main__':
    try:
        print('Starting RPLidar')
        for scan in lidar.iter_scans():
            process_data(scan)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print('Stopping RPLidar and disconnecting Arduino')
        lidar.stop()
        lidar.disconnect()
        arduino.close()
