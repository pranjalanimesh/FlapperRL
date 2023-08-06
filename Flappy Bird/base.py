from settings import *
import pygame
from pygame.locals import *

class Base:
    
    def __init__(self, image, xpos):

        #Image of ground
        self.image = image

        #Position of ground
        self.pos = self.image.get_rect()

        #Set position of ground
        self.pos[0] = xpos
        self.pos[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def draw(self, screen):
        screen.blit(self.image, self.pos)
