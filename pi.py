import os
import sys
import shlex
import shutil
import pygame

from subprocess import Popen

FILENAME = 'webcam.jpg'
CAPTUREDFILENAME = 'captured.jpg'
COMMAND = ['fswebcam', '--device', '/dev/video0', FILENAME, '--loop', '0.1']
CWD = os.getcwd()

pygame.init()

process = Popen(COMMAND, shell=False)

screen = pygame.display.set_mode((640, 640), 0)

quit_rect = pygame.draw.rect(screen, (255, 0, 0), (0, 480, 100, 80))
capture_rect = pygame.draw.rect(screen, (128, 0, 0), (100, 480, 100, 80))
pygame.display.flip()

while True:

    image = pygame.image.load(FILENAME)
    try:
        image = pygame.transform.scale(image, (640, 480))
    except:
        print('Image IO error')
        
    screen.blit(image, (0, 0))

    pygame.display.update()

    pos = pygame.mouse.get_pos()
    pressed_l, pressed_m, pressed_r = pygame.mouse.get_pressed()

    if capture_rect.collidepoint(pos) and pressed_l:
        src_file = os.path.join(CWD, FILENAME)
        dst_file = os.path.join(CWD, CAPTUREDFILENAME)
        shutil.copyfile(src_file, dst_file)

        captured = pygame.image.load(dst_file)
        captured = pygame.transform.scale(captured, (64, 64))

        screen.blit(captured, (200, 480))

    if quit_rect.collidepoint(pos) and pressed_l:
        pygame.quit()
        process.kill()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            process.kill()
            sys.exit()
