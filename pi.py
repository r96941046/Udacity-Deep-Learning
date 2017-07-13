import sys
import pygame
import pygame.camera

pygame.init()
pygame.camera.init()

screen = pygame.display.set_mode((640, 480), 0)

cam_list = pygame.camera.list_cameras()

webcam = pygame.Camera(cam_list[0], (32, 24))
webcam.start()

while True:

    image = webcam.get_image()
    image = pygame.transform.scale(image, (640, 480))
    screen.blit(image, (0, 0))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            webcam.stop()
            pygame.quit()
            sys.exit()
