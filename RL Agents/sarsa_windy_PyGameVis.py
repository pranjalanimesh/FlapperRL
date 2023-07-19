import numpy as np
import pandas as pd
import pygame
import time
import sys
import random


screen_width, screen_height = 500, 400
grid_size = 50
num_rows = screen_height // grid_size
num_cols = screen_width // grid_size
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

wind = [0,0,0,1,1,1,2,2,1,0]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.col * grid_size, self.row * grid_size, grid_size, grid_size))

    def move(self, action):
        if action == 0 or action=='up':
            self.row -= 1+wind[self.col]
        elif action == 1 or action=='down':
            self.row += 1-wind[self.col]
        elif action == 2 or action=='left':
            self.row -= wind[self.col]
            self.col -= 1
        elif action == 3 or action=='right':
            self.row -= wind[self.col]
            self.col += 1

        # Boundary conditions
        if self.row < 0:
            self.row = 0
        elif self.row > num_rows - 2:
            self.row = num_rows - 2
        elif self.col < 0:
            self.col = 0
        elif self.col > num_cols - 1:
            self.col = num_cols - 1

player = Player(0, 0)  # Starting position of the player
def display(player):
    pygame.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        # Draw the grid
        for row in range(num_rows-1):
            for col in range(num_cols):
                pygame.draw.rect(screen, BLACK, (col * grid_size, row * grid_size, grid_size, grid_size), 1)

        # Write the wind values
        try:
            for col in range(num_cols):
                font = pygame.font.Font('freesansbold.ttf', 20)
                text = font.render(str(wind[col]), True, BLACK)
                textRect = text.get_rect()
                textRect.center = (col * grid_size + grid_size // 2, (num_rows - 1) * grid_size + grid_size // 2)
                screen.blit(text, textRect)
        except:
            print('Error in wind values')

        # take inputs from the user
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move('up')
        elif keys[pygame.K_s]:
            player.move('down')
        elif keys[pygame.K_a]:
            player.move('left')
        elif keys[pygame.K_d]:
            player.move('right')

        # Draw the player
        player.draw()
        time.sleep(0.04)
        # print('player drawn')

        pygame.display.flip()
        clock.tick(60)

# display(player)
mdp = pd.DataFrame(columns=['initial_state', 'action', 'final_state', 'reward', 'prob'])
player=Player(0,0)
for row in range(num_rows-1):
    for col in range(num_cols):
        for action in range(4):
            player.row=row
            player.col=col
            player.move(action)
            if (player.row,player.col) == (row,col):
                mdp.loc[len(mdp)] = [num_cols*row+col , action, num_cols*player.row+player.col, -2, 1]
            elif (player.row,player.col) == (3,7):
                mdp.loc[len(mdp)] = [num_cols*row+col , action, num_cols*player.row+player.col, 1000, 1]
            else:
                mdp.loc[len(mdp)] = [num_cols*row+col , action, num_cols*player.row+player.col, -1, 1]

mdp.to_csv('mdp.csv', index=False)

alpha = 0.9 # learning rate
gamma = 0.9 # discount factor
epsilon = 0.4 # epsilon-greedy policy
max_episodes = 1000 # maximum number of episodes
max_steps = 1000 # maximum number of steps per episode
intitial_state = 3*num_cols # initial state

Q = np.random.random((((num_rows-1)*num_cols),4))

arrows = {
    0: '^',
    1: 'v',
    2: '<-',
    3: '->'
}

pygame.init()
pygame.display.set_caption("SARSA Agent")
running = 1
for _ in range(max_episodes):
    player.row = 3
    player.col = 0
    total_reward = 0 
    for __ in range(max_steps):
        # Event handling loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = 0
                exit()
        if not running:
            break

        random_num = np.random.rand()
        current_state = player.row*num_cols+player.col
        current_action = np.argmax(Q[current_state]) if random_num > epsilon else np.random.randint(4)

        # SARSA
        player.move(current_action)
        next_state = player.row*num_cols+player.col
        next_action = np.argmax(Q[next_state])
        # print(mdp[(mdp['initial_state']==current_state) & (mdp['action']==current_action) & (mdp['final_state']==next_state)]['reward'])
        # print(current_state, current_action, next_state, next_action)
        Q[current_state][current_action] += alpha * (mdp[(mdp['initial_state']==current_state) & (mdp['action']==current_action) & (mdp['final_state']==next_state)]['reward'].values[0] + gamma * Q[next_state][next_action] - Q[current_state][current_action])
        total_reward+=mdp[(mdp['initial_state']==current_state) & (mdp['action']==current_action) & (mdp['final_state']==next_state)]['reward'].values[0]
        screen.fill(WHITE)
        player.draw()
        # Draw the grid
        for row in range(num_rows-1):
            for col in range(num_cols):
                pygame.draw.rect(screen, BLACK, (col * grid_size, row * grid_size, grid_size, grid_size), 1)
                font = pygame.font.Font('freesansbold.ttf', 30)
                text = font.render(arrows[np.argmax(Q[row*num_cols+col])], True, BLACK)
                # # print(arrows[np.argmax(Q[player.row*num_cols+player.col])])
                textRect = text.get_rect()
                textRect.center = (col * grid_size + grid_size // 2, row * grid_size + grid_size // 2)
                screen.blit(text, textRect)

                if (row,col) == (3,7):
                    pygame.draw.rect(screen, (40,200,20), (col * grid_size, row * grid_size, grid_size, grid_size), 5)
                elif (row,col) == (3,0):
                    pygame.draw.rect(screen, (230,20,20 ), (col * grid_size, row * grid_size, grid_size, grid_size), 5)
        # Write the wind values
        for col in range(num_cols):
            font = pygame.font.Font('freesansbold.ttf', 20)
            text = font.render(str(wind[col]), True, BLACK)
            textRect = text.get_rect()
            textRect.center = (col * grid_size + grid_size // 2, (num_rows - 1) * grid_size + grid_size // 2)
            screen.blit(text, textRect)

        # time.sleep(0.04)
        pygame.display.flip()

        # Draw the player
        # clock.tick(1000)

        if player.row == 3 and player.col == 7:
            break
    print('Episode: ', _, 'Total Reward: ', total_reward)
    if not running:
        break

# pygame.quit()
