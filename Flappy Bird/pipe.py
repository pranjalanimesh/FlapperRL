from settings import *
import pygame
from pygame.locals import *

class Pipe:

    def __init__(self, image, inverted, xpos, ysize):

        #Image of pipe
        self.image = image

        #Position of pipe
        self.pos = self.image.get_rect()

        #Set pipe position
        self.inverted = inverted
        self.pos[0] = xpos
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.pos[1] = - (self.pos[3] - ysize)
        else:
            self.pos[1] = SCREEN_HEIGHT - ysize

    def update(self):
        self.pos[0] -= GAME_SPEED
        # if pos kleiner 1 delete itself

    def draw(self, screen):
        screen.blit(self.image, self.pos)

    