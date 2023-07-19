import argparse
import numpy as np
from scipy.optimize import linprog

# write a function to read the MDP file
# return the following:
# num_states: number of states in the MDP
# num_actions: number of actions in the MDP
# start_state: the start state of the MDP
# end_states: list of terminal states in the MDP
# transP: transition probabilities
# rewards: rewards
# mdptype: episodic or continuing
# discount: discount factor

def read_mdp_file(file_path):
    with open(file_path, 'r', encoding='UTF-16') as f:
        lines = f.readlines()
    
    lineArr = lines
    # print(lines[1])
    # print('running')
    num_states = int(lines[0].split()[1])
    num_actions = int(lines[1].split()[1])
    start_state = int(lines[2].split()[1])
    end_states = list(map(int, lines[3].split()[1:]))
    
    transP = np.zeros((num_states, num_actions, num_states))
    rewards = np.zeros((num_states, num_actions, num_states))
    
    for line in lines[4:-2]:
        parts = line.split()
        s1 = int(parts[1])
        ac = int(parts[2])
        s2 = int(parts[3])
        r = eval(parts[4])
        p = eval(parts[5])
        rewards[s1, ac, s2] = r
        transP[s1, ac, s2] = p
    
    mdptype = lines[-2].split()[1]
    discount = float(lines[-1].split()[1])
    # if(mdptype =='episodic'):
    #     discount = 1
    # print('Read the file')
    return num_states, num_actions, start_state, end_states, transP, rewards, mdptype, discount

def value_iteration(num_states, num_actions, transitions, rewards, discount_factor):
    values = np.zeros(num_states)
    policy = np.zeros(num_states, dtype=int)
    
    while True:
        prev_values = values.copy()
        
        for state in range(num_states):
            q_values = np.array([-10000]*num_actions)
            
            for action in range(num_actions):
                q_value = 0.0
                
                for next_state in range(num_states):
                    q_value += transitions[state, action, next_state] * (rewards[state, action, next_state] + discount_factor * prev_values[next_state])
                
                q_values[action] = q_value
            
            best_action = np.argmax(q_values)
            values[state] = q_values[best_action]
            policy[state] = best_action
        
        if np.max(np.abs(values - prev_values)) < 1e-8:
            break
    
    return values, policy

def howards_policy_iteration(num_states, num_actions, transitions, rewards, discount_factor):
    values = np.zeros(num_states)
    policy = np.zeros(num_states, dtype=int)
    
    while True:
        # print('policy evaluation')
        # Policy evaluation
        while True:
            prev_values = values.copy()
            
            for state in range(num_states):
                # print(state)
                action = policy[state]
                
                value = 0.0
                for next_state in range(num_states):
                    value += transitions[state, action, next_state] * (rewards[state, action, next_state] + discount_factor * prev_values[next_state])
                
                values[state] = value
            
            if np.max(np.abs(values - prev_values)) < 1e-7:
                break
        
        # Policy improvement
        # print('policy improving')
        policy_stable = True
        
        for state in range(num_states):
            old_action = policy[state]
            q_values = np.zeros(num_actions)
            
            for action in range(num_actions):
                q_value = 0.0
                
                for next_state in range(num_states):
                    q_value += transitions[state, action, next_state] * (rewards[state, action, next_state] + discount_factor * values[next_state])
                
                q_values[action] = q_value
            
            best_action = np.argmax(q_values)
            policy[state] = best_action
            
            if old_action != best_action:
                policy_stable = False
        # print('Policy improved')
        
        if policy_stable:
            break
    return values, policy

def linear_programming(num_states, num_actions, transitions, rewards, discount_factor):
    c = np.zeros(num_states)
    A_ub = np.zeros((num_states * num_actions, num_states))
    b_ub = np.zeros(num_states * num_actions)
    bounds = [(None, None)] * num_states
    
    for state in range(num_states):
        c[state] = -1.0
        
        for action in range(num_actions):
            b_ub[state * num_actions + action] = 0.0
            
            for next_state in range(num_states):
                A_ub[state * num_actions + action, next_state] = transitions[state, action, next_state]
                b_ub[state * num_actions + action] += transitions[state, action, next_state] * (rewards[state, action, next_state] + discount_factor * 0.0)
    
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method='highs')
    
    values = result.x
    policy = np.zeros(num_states, dtype=int)
    
    for state in range(num_states):
        q_values = np.zeros(num_actions)
        
        for action in range(num_actions):
            q_value = 0.0
            
            for next_state in range(num_states):
                try:
                    q_value += transitions[state, action, next_state] * (rewards[state, action, next_state] + discount_factor * values[next_state])
                except:
                    q_value +=0

            q_values[action] = q_value
        
        best_action = np.argmax(q_values)
        policy[state] = best_action
    
    return values, policy

def print_results(values, policy):
    for state in range(len(values)):
        value = values[state]
        action = policy[state]
        # print(f"V*({state})   π*({state})")
        print(f"{value:.6f}   {action}")

def main():
    # Read command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--mdp", help="Path to the MDP txt file")
    parser.add_argument("--algorithm", help="Algorithm to solve the MDP (vi, hpi, lp)")
    args = parser.parse_args()

    mdp_file = args.mdp
    algorithm = args.algorithm
    
    # Read MDP file
    num_states, num_actions, start_state, end_states, transitions, rewards, mdptype, discount = read_mdp_file(mdp_file)
    
    # Solve MDP using the specified algorithm
    if algorithm == "vi":
        values, policy = value_iteration(num_states, num_actions, transitions, rewards, discount)
    elif algorithm == "hpi":
        values, policy = howards_policy_iteration(num_states, num_actions, transitions, rewards, discount)
    elif algorithm == "lp":
        values, policy = linear_programming(num_states, num_actions, transitions, rewards, discount)
    else:
        print("Invalid algorithm specified. Please choose either 'vi', 'hpi', or 'lp'.")
        return
    
    # Print the optimal value function and policy
    print_results(values, policy)

if __name__ == "__main__":
    main()
