import pygame
import time
import random  # Thêm thư viện random

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước cửa sổ hiển thị (vừa với độ phân giải hình ảnh)
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Robot Blinking Eyes")

# Tải các hình ảnh (với kích thước 1280x720)
open_eye = pygame.image.load('mo_mat.png')
closed_eye = pygame.image.load('nham_mat.png')

# Vị trí của mắt trên màn hình (center align)
eye_x = 0
eye_y = 0

# Thiết lập màu nền
background_color = (0, 0, 0)  # Màu đen

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hiển thị hình ảnh mở mắt
    screen.fill(background_color)
    screen.blit(open_eye, (eye_x, eye_y))
    pygame.display.flip()
    
    # Thời gian ngẫu nhiên cho trạng thái mở mắt
    open_time = random.uniform(2, 5)  # Thời gian ngẫu nhiên từ 2 đến 5 giây
    time.sleep(open_time)
    
    # Thực hiện chớp mắt tối đa 2 lần liên tục
    for _ in range(random.randint(1, 2)):  # Số lần chớp mắt ngẫu nhiên từ 1 đến 2 lần
        # Hiển thị hình ảnh nhắm mắt
        screen.fill(background_color)
        screen.blit(closed_eye, (eye_x, eye_y))
        pygame.display.flip()
        time.sleep(random.uniform(0.05, 0.2))  # Thời gian nhắm mắt ngẫu nhiên từ 0.05 đến 0.2 giây

        # Hiển thị hình ảnh mở mắt
        screen.fill(background_color)
        screen.blit(open_eye, (eye_x, eye_y))
        pygame.display.flip()
        time.sleep(random.uniform(0.05, 0.2))  # Thời gian mở mắt ngẫu nhiên từ 0.05 đến 0.2 giây

# Kết thúc Pygame
pygame.quit()
