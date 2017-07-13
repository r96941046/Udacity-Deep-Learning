import sys
import shlex
import pygame

from subprocess import call

FILENAME = 'webcam.jpg'

pygame.init()

call(shlex.split('fswebcam --device /dev/video0 --loop 1 ' + FILENAME))

screen = pygame.display.set_mode((640, 480), 0)

while True:

    image = pygame.image.load(FILENAME)
    image = pygame.transform.scale(image, (640, 480))
    screen.blit(image, (0, 0))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
