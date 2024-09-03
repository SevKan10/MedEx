import pygame
import sys
import time

# Khởi tạo Pygame
pygame.init()

# Thiết lập kích thước màn hình
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cute Tech Eyes")

# Màu sắc
background_color = (0, 0, 0)  # Màu nền đen
eye_color = (100, 149, 237)    # Màu mắt (cornflower blue)
pupil_color = (0, 0, 0)        # Màu con ngươi đen

# Kích thước và hiệu ứng
eye_width = 150
eye_height = 100
corner_radius = 30
blink_duration = 0.2  # Thời gian chớp mắt (giây)
blink_interval = 1  # Thời gian giữa các lần chớp mắt (giây)

def draw_eye(blink_progress):
    screen.fill(background_color)  # Làm nền đen

    # Tính toán chiều cao của mắt khi chớp
    eye_rect = pygame.Rect(300, 250, eye_width, eye_height)
    if blink_progress < 0.5:  # Đang nhắm mắt
        eye_rect.height = int(eye_height * (1 - 2 * blink_progress))
    else:  # Đang mở mắt
        eye_rect.height = int(eye_height * (2 * blink_progress - 1))
    
    # Vẽ mắt trái
    pygame.draw.rect(screen, eye_color, eye_rect, border_radius=corner_radius)
    if blink_progress >= 0.5:  # Khi mắt mở
        pygame.draw.ellipse(screen, pupil_color, (375, 275, 40, 40))  # Con ngươi trái

    # Vẽ mắt phải
    eye_rect.x = 450
    pygame.draw.rect(screen, eye_color, eye_rect, border_radius=corner_radius)
    if blink_progress >= 0.5:  # Khi mắt mở
        pygame.draw.ellipse(screen, pupil_color, (525, 275, 40, 40))  # Con ngươi phải

    # Vẽ hiệu ứng ánh sáng cho mắt
    pygame.draw.ellipse(screen, (255, 255, 255, 100), (340, 260, 30, 30))  # Ánh sáng mắt trái
    pygame.draw.ellipse(screen, (255, 255, 255, 100), (590, 260, 30, 30))  # Ánh sáng mắt phải

# Vòng lặp chính
last_blink_time = time.time()
blink_start_time = last_blink_time
blinking = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    current_time = time.time()
    elapsed_time = current_time - last_blink_time

    if elapsed_time >= blink_interval:
        if not blinking:
            blink_start_time = current_time
            blinking = True
    else:
        if blinking:
            blink_progress = (current_time - blink_start_time) / blink_duration
            if blink_progress > 1:
                blink_progress = 1
                blinking = False
                last_blink_time = current_time
        else:
            blink_progress = 1  # Mắt không chớp, vẫn mở

    draw_eye(blink_progress)
    pygame.display.flip()
    pygame.time.delay(10)  # Delay để tạo hiệu ứng mượt mà
