from rplidar import RPLidar

# Khởi tạo kết nối với Lidar
lidar = RPLidar('COM16')

# Lấy thông tin và sức khỏe của Lidar
info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)

try:
    # Vòng lặp liên tục để quét dữ liệu Lidar
    for i, scan in enumerate(lidar.iter_scans()):
        print('Scan number: %d' % i)
        for measurement in scan:
            quality, angle, distance = measurement
            print('Góc: %.2f°, Khoảng cách: %.2f mm, Chất lượng: %d' % (angle, distance, quality))
finally:
    # Dừng Lidar và ngắt kết nối (sẽ chạy khi thoát bằng Ctrl+C)
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
