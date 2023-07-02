# Write flappy bird game
import pygame
import random
import sys
from os import path # for loading images

# set up assets folders
assetsDir = path.join(path.dirname(__file__), 'assets')

# Define Player
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.velocity = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.image = pygame.image.load(path.join(assetsDir, image_path))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        self.velocity = self.jump_power

    def draw(self, screen):
        screen.blit(self.image, self.rect)
