# Write flappy bird game
import pygame
import random
import sys
from player import *
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

# add code for the game
class FlappyBirdGame():
    def __init__(self) -> None:
        # initialize pygame
        pygame.init()
        # set the width and height of the screen
        screen_width = 288
        screen_height = 512
        screen_width = 288*1.5
        screen_height = 512*1.5
        self.screen = pygame.display.set_mode((screen_width, screen_height),pygame.NOFRAME)
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.isRunning = True
        self.all_sprites = pygame.sprite.Group()
        self.player = Player(10,10,'bird1.png')
        self.background = Background(0,0,'background-night-scaled-1.5.png')
        self.all_sprites.add(self.background)
        self.all_sprites.add(self.player)
    
    def run(self):
        self.isRunning = True

        while(self.isRunning):
            self.handleEvents()
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.isRunning = False
            # Handle other events here
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.player.jump()

    def update(self):
        # Update game state here
        self.all_sprites.update()
        # Move sprites here

        # Check for collisions here

    def render(self):
        # Draw sprites here
        # self.all_sprites.draw(self.screen)
        # Update display here

        # Draw Player
        # self.player.draw(self.screen)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()


game = FlappyBirdGame()
game.run()