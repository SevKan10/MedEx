import pygame
import random
import time

pygame.init()

# Thiết lập kích thước cửa sổ hiển thị
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Emotion Display")


images = {
    'mo_mat': pygame.image.load('images/mo_mat.png'),
    'nham_mat': pygame.image.load('images/nham_mat.png'),
    'mo_phai': pygame.image.load('images/mo_phai.png'),
    'mo_trai': pygame.image.load('images/mo_trai.png'),
    'nheo_mat': pygame.image.load('images/nheo_mat.png')
}

def display_image(image_key, delay=2):
    """ Hiển thị hình ảnh và chờ một khoảng thời gian """
    screen.fill((0, 0, 0))  # Xóa màn hình với màu đen
    screen.blit(images[image_key], (0, 0))
    pygame.display.flip()
    time.sleep(delay)

def blink_eye():
    """ Hiệu ứng chớp mắt """
    display_image('mo_mat')
    time.sleep(0.5)
    display_image('mo_phai', 0.1)
    display_image('nham_mat', 0.1)
    display_image('mo_trai', 0.1)
    display_image('mo_mat', 1)

def tuc_cute_face():
    """ Hiệu ứng cảm xúc đáng yêu """
    display_image('mo_mat')
    display_image('nham_mat', 0.5)
    display_image('mo_mat', 0.5)

def khoc_face():
    """ Hiệu ứng cảm xúc buồn """
    display_image('mo_mat')
    display_image('nham_mat', 0.5)
    display_image('mo_mat', 0.5)

def cuoi_face():
    """ Hiệu ứng cảm xúc vui vẻ """
    display_image('mo_mat')
    display_image('nham_mat', 0.5)
    display_image('mo_mat', 0.5)

def the_rock_face():
    """ Hiệu ứng cảm xúc giống The Rock """
    display_image('mo_mat')
    display_image('nham_mat', 0.5)
    display_image('nheo_mat', 1)
    display_image('nham_mat', 0.5)
    display_image('mo_mat', 0.5)

def setup():
    pygame.display.set_caption("Emotion Display")
    screen.fill((0, 0, 0))
    pygame.display.flip()

def loop():

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Chọn ngẫu nhiên một trong các hình ảnh
        random_choice = random.choice([blink_eye, tuc_cute_face, khoc_face, cuoi_face, the_rock_face])
        random_choice()
        time.sleep(1)  

if __name__ == "__main__":
    setup()
    loop()
