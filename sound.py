import os

import pygame

from pygame import event
from pygame import mixer


pygame.init()
mixer.init()

path = os.path.dirname(os.path.abspath(__file__))
file = os.path.join(path, 'test.mp3')

mixer.music.load(file)
mixer.music.play()

event.wait()
