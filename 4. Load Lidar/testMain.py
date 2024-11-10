import rplidar
import serial
import time

# Khởi tạo kết nối với LIDAR và Arduino
LIDAR_PORT = 'COM16'  # Thay đổi nếu cần
ARDUINO_PORT = 'COM21'  # Thay đổi nếu cần
BAUD_RATE = 115200
MIN_DISTANCE = 300  # 30 cm, ngưỡng khoảng cách tối thiểu

# Khởi tạo kết nối với LIDAR và cổng serial Arduino
lidar = rplidar.RPLidar(LIDAR_PORT, baudrate=BAUD_RATE)
ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Đợi Arduino khởi động

# Hàm gửi lệnh đến Arduino
def send_to_arduino(command):
    ser.write(f"{command}\n".encode())
    print(f"Sent to Arduino: {command}")

# Hàm kiểm tra vật cản và quyết định hướng đi
def check_obstacle(scan_data):
    # Chia dữ liệu thành các vùng: trước, trái, phải
    front_range = []
    left_range = []
    right_range = []

    for scan in scan_data:
        angle = scan[1]
        distance = scan[2]

        if distance == 0:  # Bỏ qua giá trị không hợp lệ
            continue

        # Phân chia dữ liệu LIDAR vào các vùng khác nhau
        if 331 <= angle <= 360 or 0 <= angle <= 29:  # Vùng trước
            front_range.append(distance)
        elif 250 <= angle <= 330:  # Vùng bên trái
            left_range.append(distance)
        elif 30 <= angle <= 109:  # Vùng bên phải
            right_range.append(distance)

    # Tính khoảng cách trung bình của mỗi vùng
    avg_front = sum(front_range) / len(front_range) if front_range else float('inf')
    avg_left = sum(left_range) / len(left_range) if left_range else float('inf')
    avg_right = sum(right_range) / len(right_range) if right_range else float('inf')

    # Kiểm tra và trả về lệnh điều khiển
    if avg_front < MIN_DISTANCE:  # Nếu có vật cản trước, dừng lại
        send_to_arduino('T,0,0')  # Gửi lệnh dừng đến Arduino
        time.sleep(1)  # Dừng trong 1 giây
        # Sau khi dừng, quyết định rẽ trái hoặc phải
        if avg_left >= MIN_DISTANCE:
            return 'L,200,200'  # Rẽ trái nếu bên trái không có vật cản
        elif avg_right >= MIN_DISTANCE:
            return 'R,200,200'  # Rẽ phải nếu bên phải không có vật cản
        if avg_left > avg_right:
            return 'L,200,200'  # Rẽ trái nếu khoảng cách bên trái lớn hơn
        else:
            return 'R,200,200'  # Rẽ phải nếu khoảng cách bên phải lớn hơn
    else:
        # Nếu không có vật cản phía trước, đi thẳng
        return 'S,200,200'

# Vòng lặp chính
try:
    for scan in lidar.iter_scans():
        # Xử lý dữ liệu LIDAR
        command = check_obstacle(scan)
        send_to_arduino(command)  # Gửi lệnh đến Arduino
        time.sleep(0.1)

except KeyboardInterrupt:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    ser.close()
    print("Stopping LIDAR and Arduino connection")
