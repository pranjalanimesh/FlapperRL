from pygame.locals import *
from os import path # for loading images
from settings import *
import pygame

class Player:

    def __init__(self, image):

        #Image of bird
        self.image =  image

        #Vertical speed of bird
        self.speed = SPEED

        #Position of bird
        self.pos = self.image.get_rect() # Position # left,top, width, height

        #Set position of bird
        self.pos[0] = round(SCREEN_WIDHT / 6 / GAME_SPEED) * GAME_SPEED #ensure divisible trough GAME_SPEED -> used for score function
        self.pos[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.speed += GRAVITY
        self.pos[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def draw(self, screen):
        screen.blit(self.image, self.pos)

