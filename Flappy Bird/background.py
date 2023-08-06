from settings import *
import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image_path):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.image = pygame.image.load(path.join(assetsDir, image_path))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)