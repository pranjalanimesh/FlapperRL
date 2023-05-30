import argparse

# Define the actions
ACTIONS = ['N', 'S', 'E', 'W']

def parse_grid_file(gridfile):
    """
    Parse the grid file and return the grid as a 2D list.
    """
    grid = []
    with open(gridfile, 'r') as file:
        for line in file:
            row = line.strip().split()
            grid.append(row)
    return grid

def is_valid_move(grid, x, y, action):
    """
    Check if a move is valid in the given grid.
    """
    rows, cols = len(grid), len(grid[0])
    if action == 'N':
        return x > 0 and grid[x - 1][y] != '1'
    elif action == 'S':
        return x < rows - 1 and grid[x + 1][y] != '1'
    elif action == 'E':
        return y < cols - 1 and grid[x][y + 1] != '1'
    elif action == 'W':
        return y > 0 and grid[x][y - 1] != '1'
    return False

def encode_maze_as_mdp(gridfile):
    """
    Encode the maze as an MDP and output the MDP file.
    """
    grid = parse_grid_file(gridfile)
    rows, cols = len(grid), len(grid[0])
    num_states = rows * cols
    num_actions = len(ACTIONS)

    # Initialize the MDP string
    mdp_string = f"numStates {num_states}\n"
    mdp_string += f"numActions {num_actions}\n"

    # Get the start states
    start_states = []
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == '2':
                start_states.append(x * cols + y)
    mdp_string += "start " + " ".join(str(state) for state in start_states) + "\n"

    # mdp_string += "start 0\n"

    # Get the end states
    end_states = []
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == '3':
                end_states.append(x * cols + y)
    mdp_string += "end " + " ".join(str(state) for state in end_states) + "\n"

    # Encode transitions and rewards
    for state in range(num_states):
        x, y = divmod(state, cols)
        for action_index, action in enumerate(ACTIONS):
            if is_valid_move(grid, x, y, action):
                if action == 'N':
                    new_state = state - cols
                elif action == 'S':
                    new_state = state + cols
                elif action == 'E':
                    new_state = state + 1
                elif action == 'W':
                    new_state = state - 1

                new_x , new_y = divmod(new_state,cols)
                if grid[x][y] in ['0','2']:
                    if grid[new_x][new_y]=='0':
                        mdp_string += f"transition {state} {action_index} {new_state} -1 1.0\n"
                    if grid[new_x][new_y]=='2':
                        mdp_string += f"transition {state} {action_index} {new_state} -2 1.0\n"
                    if grid[new_x][new_y]=='3':
                        mdp_string += f"transition {state} {action_index} {new_state} 1000000 1.0\n"

    # Add the MDP type and discount factor
    mdp_string += "mdptype episodic\n"
    mdp_string += "discount 1.0"

    return mdp_string

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Encode a maze as an MDP')
    parser.add_argument('--grid', help='Maze grid file path', required=True)
    args = parser.parse_args()

    # Encode the maze as an MDP
    mdp_string = encode_maze_as_mdp(args.grid)

    # Output the MDP
    print(mdp_string)
    return mdp_string

if __name__ == '__main__':
    # text_file = open("mdpfile.txt", "w")
    # n = text_file.write(main())
    # text_file.close()
    main()
