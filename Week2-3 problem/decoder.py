import argparse
import numpy as np
from encoder import parse_grid_file, ACTIONS

def read_value_policy(value_policy_file):
    value = []
    policy = []
    with open(value_policy_file, 'r', encoding='UTF-16') as file:
        for line in file:
            v = float(line.strip().split()[0])
            p = int(line.strip().split()[1])
            value.append(v)
            policy.append(p)
    return value,policy

if __name__ == "__main__":
    # Read command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid", help="Path to the grid file")
    parser.add_argument("--value_policy", help="Path to the value and policy file")
    args = parser.parse_args()

    grid = parse_grid_file(args.grid)
    value,policy = read_value_policy(args.value_policy)
    
    rows, cols = len(grid), len(grid[0])
    num_states = rows * cols
    # Get the start state
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == '2':
                start_state = (x * cols + y)

    # Get the end state
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == '3':
                end_state=(x * cols + y)

    path = []
    state = start_state
    while state!= end_state:
        action = ACTIONS[policy[state]]
        path.append(action)
        if action == 'N':
            state = state - cols
        elif action == 'S':
            state = state + cols
        elif action == 'E':
            state = state + 1
        elif action == 'W':
            state = state - 1
    print(' '.join(path))
    # print(value)
    # print(len(value)) 
    # print(policy)
    # print(len(policy))


