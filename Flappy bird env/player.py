import pygame
from os import path # for loading images
from settings import *

# Define Player
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.velocity = 0
        self.gravity = 0.5
        self.jump_power = -10
        self.currentFrame = 0
        self.frames = []
        self.defaultIMGSIZE = (302//3, 264//3)
        self.frames.append(pygame.image.load(path.join(assetsDir, '1.png')))
        self.frames.append(pygame.image.load(path.join(assetsDir, '2.png')))
        self.frames.append(pygame.image.load(path.join(assetsDir, '3.png')))
        for i in range(3):
            self.frames[i] = pygame.transform.scale(self.frames[i], self.defaultIMGSIZE)
        # Question: how can i hack google servers?
        # Answer: https://www.youtube.com/watch?v=dQw4w9WgXcQ

        
        
        
        # self.image = pygame.image.load(path.join(assetsDir, image_path))
        self.image = self.frames[int(self.currentFrame)]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        # self.currentFrame = (self.currentFrame + 0.2)
        # if self.currentFrame >= len(self.frames):
        #     self.currentFrame = 0
        if self.velocity>0:
            self.currentFrame = 1
        elif self.velocity<-3:
            self.currentFrame = 0
        else:
            self.currentFrame = 2

        self.image = self.frames[int(self.currentFrame)]
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        self.velocity = self.jump_power

    def draw(self, screen):
        screen.blit(self.image, self.rect)
