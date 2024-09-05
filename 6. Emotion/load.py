import pygame
import time

pygame.init()

# Thiết lập kích thước cửa sổ hiển thị
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Emotion Display")


images = {
    '1': pygame.image.load('images/load1.png'),
    '2': pygame.image.load('images/load2.png'),
    '3': pygame.image.load('images/load3.png')
}

def display_image(image_key, delay=2):
    """ Hiển thị hình ảnh và chờ một khoảng thời gian """
    screen.fill((0, 0, 0))  # Xóa màn hình với màu đen
    screen.blit(images[image_key], (0, 0))
    pygame.display.flip()
    time.sleep(delay)

def load():
    display_image('1')
    display_image('2', 0.1)
    display_image('3', 0.5)
    
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
        load()
        time.sleep(1)  

if __name__ == "__main__":
    setup()
    loop()
