import serial
from rplidar import RPLidar
import numpy as np
import time

# Constants
LIDAR_PORT = 'COM16'  # Replace with your Lidar sensor port
ARDUINO_PORT = 'COM20'  # Replace with your Arduino communication port
BAUDRATE = 115200

# Smooth Filter Class
class SmoothFilter:
    def __init__(self, size):
        self.size = size
        self.data = []

    def add(self, value):
        self.data.append(value)
        if len(self.data) > self.size:
            self.data.pop(0)
        return np.mean(self.data)

# Initialize Lidar and Arduino
lidar = RPLidar(LIDAR_PORT)
arduino = serial.Serial(ARDUINO_PORT, BAUDRATE, timeout=1)

# Initialize filters and timing
distance_filter = SmoothFilter(5)
angle_filter = SmoothFilter(5)
last_command = None
last_command_time = 0
command_cooldown = 0.5  # seconds

def control_robot(angle, distance):
    global last_command
    global last_command_time
    
    current_time = time.time()
    smoothed_distance = distance_filter.add(distance)
    smoothed_angle = angle_filter.add(angle)
    
    if smoothed_distance < 500:
        # Add dead zones to reduce sensitivity
        if smoothed_angle < 165 or smoothed_angle > 195:
            if smoothed_angle <= 180:
                command = 'R,30,30\n'  # Move right if obstacle is detected in the left half
            elif smoothed_angle >= 190:
                command = 'L,30,30\n'  # Move left if obstacle is detected in the right half
            elif smoothed_angle <= 10 or smoothed_angle >= 350:
                command = 'B,30,30\n'  # Move backward if obstacle is detected in front
        else:
            command = 'S,250,250\n'  # Stop if within dead zone
        
    else:
        command = 'S,250,250\n'  # Stop if no obstacle within 500 mm
    
    if current_time - last_command_time >= command_cooldown and command != last_command:
        arduino.write(command.encode())
        last_command = command
        last_command_time = current_time

try:
    for scan in lidar.iter_scans():
        for _, angle, distance in scan:
            # Control the robot based on the current angle and distance
            control_robot(angle, distance)
finally:
    # Stop Lidar and close connections
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    arduino.close()
