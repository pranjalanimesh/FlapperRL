# Write flappy bird game
import pygame
import random
import sys
from player import *  
from background import *
from settings import *
from os import path # for loading images

# add code for the game
class FlappyBirdGame():
    def __init__(self) -> None:
        # initialize pygame
        pygame.init()
        # set the width and height of the screen
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock() 
        self.isRunning = True
        self.gameState = 'mainGame'
        self.mainGameSprites = pygame.sprite.Group()
        self.player = Player(10,10,'bird1.png')
        self.background = Background(0,0,'background-night-scaled.png')
        self.mainGameSprites.add(self.background)
        self.mainGameSprites.add(self.player)
    
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
        if self.gameState == 'mainGame':
            self.mainGameSprites.update()
        elif self.gameState == 'gameOver':
            pass

    def render(self):
        if self.gameState == 'mainGame':
            self.mainGameSprites.draw(self.screen)
        pygame.display.flip()


game = FlappyBirdGame()
game.run()