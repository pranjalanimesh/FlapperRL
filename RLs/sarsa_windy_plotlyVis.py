import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import time
import sys
import random

num_rows = 8
num_cols = 10

wind = [0,0,0,1,1,1,2,2,1,0]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col

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

player=Player(0,0)

mdp = pd.DataFrame(columns=['initial_state', 'action', 'final_state', 'reward', 'prob'])

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


alpha = 0.5 # learning rate
gamma = 0.9 # discount factor
epsilon = 0.1 # epsilon-greedy policy
max_episodes = 100 # maximum number of episodes
max_steps = 1000 # maximum number of steps per episode
initial_state = 3*num_cols # initial state

Q = np.random.random((((num_rows-1)*num_cols),4))

running = 1
history = pd.DataFrame({'rewards' : [0]}, columns=['rewards'])

for _ in range(max_episodes):
    player.row = 3
    player.col = 0
    total_reward = 0 
    for __ in range(max_steps):
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

        if player.row == 3 and player.col == 7:
            break
    print('Episode: ', _, 'Total Reward: ', total_reward)

    epsilon*= 0.999
    alpha *= 0.99
    history=history.append({'rewards': total_reward}, ignore_index=True)

    # if 980<total_reward:
    #     running = 0 
    if not running:
        break

with plt.style.context("dark_background"):
  
  fig, ax = plt.subplots()
  x = np.linspace(-10, 10, 100)
  
  ax.plot(history['rewards'], label='rewards')
  plt.show()