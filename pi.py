import os
import sys
import shutil
import tensorflow as tf
import pygame
import numpy as np

from scipy import ndimage
from scipy.misc import imresize
from subprocess import Popen

FILENAME = 'webcam.jpg'
CAPTUREDFILENAME = 'captured.jpg'
COMMAND = ['fswebcam', '--no-banner', '--device', '/dev/video0', FILENAME, '--loop', '1']
CWD = os.getcwd()

PIXEL_DEPTH = 255.0
IMAGE_SIZE = 32
MAX_DIGITS = 5

pygame.init()

process = Popen(COMMAND, shell=False)

screen = pygame.display.set_mode((640, 640), 0)

quit_rect = pygame.draw.rect(screen, (255, 0, 0), (0, 480, 100, 80))
capture_rect = pygame.draw.rect(screen, (128, 0, 0), (100, 480, 100, 80))
pygame.display.flip()

while True:

    try:
        image = pygame.image.load(FILENAME)
        image = pygame.transform.scale(image, (640, 480))
    except:
        print('Image IO error')

    screen.blit(image, (0, 0))

    pygame.display.update()

    pos = pygame.mouse.get_pos()
    pressed_l, pressed_m, pressed_r = pygame.mouse.get_pressed()

    if capture_rect.collidepoint(pos) and pressed_l:

        print('Analyzing...')
        
        src_file = os.path.join(CWD, FILENAME)
        dst_file = os.path.join(CWD, CAPTUREDFILENAME)
        shutil.copyfile(src_file, dst_file)

        captured = pygame.image.load(dst_file)
        captured = pygame.transform.scale(captured, (64, 64))

        screen.blit(captured, (200, 480))

        image_file = ndimage.imread(dst_file).astype(np.float32)
        grey = np.dot(image_file, [0.299, 0.587, 0.114])
        resized = imresize(grey, (IMAGE_SIZE, IMAGE_SIZE))
        normalized = (resized - PIXEL_DEPTH / 2) / PIXEL_DEPTH
        normalized = normalized.reshape((IMAGE_SIZE, IMAGE_SIZE, 1))

        data = np.zeros((1, IMAGE_SIZE, IMAGE_SIZE, 1), dtype=np.float32)
        data[0] = normalized

        graph = tf.get_default_graph()

        with tf.Session(graph=graph) as session:

            loader = tf.train.import_meta_graph('svhn.meta')
            loader.restore(session, tf.train.latest_checkpoint('./'))

            tf_data = graph.get_tensor_by_name('data:0')
            keep_prob = graph.get_tensor_by_name('keep_prob:0')
            prediction = graph.get_tensor_by_name('prediction:0')

            feed_dict = {
                tf_data: data,
                keep_prob: 1.0
            }

            p = prediction.eval(feed_dict)

            digitized = np.split(np.argmax(p, axis=1), MAX_DIGITS)
            digits = []

            for [digit] in digitized:
                if digit == 10:
                    digit = ''
                digits.append(str(digit))

            result = ''.join(digits)
            print('Result: %s' % result)

    if quit_rect.collidepoint(pos) and pressed_l:
        pygame.quit()
        process.kill()
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            process.kill()
            sys.exit()
