import random
from itertools import product
import os
import pickle
import re
from EasyDifficultAI import ScoreCalculation

#Initial state
sectionsForPlayers = ["One", "Two", "Three", "Four", "Five", "Six", "3 of a kind", "4 of a kind", "Full House", "Small Straight", "Large Straight", "Yahtzee", "Chance", "First 6 sections score", "Bonus", "Final Score"]
statePlayers = list(range(5))

# Constants
num_episodes = 1
epsilon = 0.5
NUM_EPISODES = 0
ALPHA = 0.9  # Learning rate
GAMMA = 0.9  # Discount factor
EPSILON = 0.6  # Exploration rate
Q_TABLE_FILE = 'q_table.pkl'  # File in which the Q-table will be saved
Q_NUM_FILE = 'num_episodes.pkl' # File in which the number of episodes will be saved

# Generate all possible dice configurations
dice_configurations = sorted(set(''.join(map(str, sorted(dice))) for dice in product(range(1, 7), repeat=5)))

# Generate all combinations of scoring categories (0=empty, 1=taken)
scoring_combinations = list(product([0, 1], repeat=13))

q_table = {}
# Load Q-table from file if it exists, otherwise initialize an empty dictionary
if os.path.exists(Q_TABLE_FILE):
    with open(Q_TABLE_FILE, 'rb') as f:
        q_table = pickle.load(f)
        with open (Q_NUM_FILE, 'rb') as num:
            NUM_EPISODES = NUM_EPISODES + pickle.load(num) # Load the number of episodes from the file
        f.close()
else:
    q_table = {}

def save_q_table():
    with open(Q_TABLE_FILE, 'wb') as f:
        pickle.dump(q_table, f)
        
def save_episodes_num(num_episodes):
    with open(Q_NUM_FILE, "wb") as f:
        pickle.dump(num_episodes, f)

def choose_action(state):
    if random.random() < 0.1:
        # Explore: Choose a random action
        return random.choice([i for i in range(0,13) if state[1][i] == 0])
    
    # Exploit: Choose the best-known action
    return max(range(13), key=lambda action: q_table.get((state, action), calculate_reward(state[0], state[1], action)/5.0) if state[1][action] == 0 else -1)

def roll_dice(held_dice=[]):
    dice = held_dice + [random.randint(1, 6) for _ in range(5 - len(held_dice))]
    return sorted(dice)

def reset_dice():
    return [0, 0, 0, 0, 0]

def calculate_reward(dice, state, action_index):
    # Define scoring rules for Yahtzee
    if action_index == 11 and state[11] == 0:  # "Yahtzee"
        return 50 if len(set(dice)) == 1 else 0
    elif action_index == 10 and state[10] == 0:  # "Large Straight"
        return 40 if sorted(dice) in ([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]) else 0
    elif action_index == 9 and state[9] == 0:  # "Small Straight"
        return 30 if any(all(x in dice for x in seq) for seq in ([1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6])) else 0
    elif action_index == 8 and state[8] == 0:  # "Full House"
        return 25 if sorted([dice.count(d) for d in set(dice)]) == [2, 3] else 0
    elif action_index == 6 and state[6] == 0:  # "Three of a Kind"
        return sum(dice) if any(dice.count(d) >= 3 for d in set(dice)) else 0
    elif action_index == 7 and state[7] == 0:  # "Four of a Kind"
        return sum(dice) if any(dice.count(d) >= 4 for d in set(dice)) else 0
    elif action_index == 0 and state[0] == 0:  # "Ones"
        return sum(d for d in dice if d == 1)
    elif action_index == 1 and state[1] == 0:  # "Twos"
        return sum(d for d in dice if d == 2)
    elif action_index == 2 and state[2] == 0:  # "Threes"
        return sum(d for d in dice if d == 3)
    elif action_index == 3 and state[3] == 0:  # "Fours"
        return sum(d for d in dice if d == 4)
    elif action_index == 4 and state[4] == 0:  # "Fives"
        return sum(d for d in dice if d == 5)
    elif action_index == 5 and state[5] == 0:  # "Sixes"
        return sum(d for d in dice if d == 6)
    elif action_index == 12 and state[12] == 0:  # "Chance"
        return sum(dice)
    return 0  # Fallback reward

def train_q_learning(): 
    for episode in range(num_episodes):
        #print("Episode " , episode + NUM_EPISODES, " started.")
        # Initialize the game state
        dices = roll_dice()
        dices.sort()
        scoring_state = tuple([0] * 13)  # All categories initially empty

        for turn in range(13):  # Maximum of 13 turns per game/episode
            #print("Turn ", turn + 1, " started.")
            # Define the current state
            current_state = (tuple(dices), scoring_state) 
            #print("Current state: ", current_state)

            # Choose an action (scoring category) using epsilon-greedy policy
            action = choose_action(current_state) 
            #print("\nAction: ", action)

            # Calculate the reward for the chosen action
            reward = calculate_reward(dices, scoring_state,  action) 
            #print("Reward: ", reward)

            #print("scoring state before: ", scoring_state)
            # Simulate scoring the chosen category (update scoring_state)
            new_scoring_state = list(scoring_state)
            if 0 <= action < len(new_scoring_state):
                new_scoring_state[action] = 1  # Mark the category as taken
            scoring_state = tuple(new_scoring_state) 
            #print("Scoring state after: ", scoring_state)

            # Roll the dice again for the next state
            dices = roll_dice()
            dices.sort()

            # Define the new state
            new_state = (tuple(dices), scoring_state)

            # Compute the maximum Q-value for the next state
            max_next_q_value = 0.0 if new_state[1] == (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) else max(
                q_table.get((new_state, act), 0.0) for act in range(13) if new_state[1][act] == 0) 
            #print("Max next Q-value: ", max_next_q_value)

            # Update Q-value using the Q-learning formula
            current_q_value = q_table.get((current_state, action), 0.0) 
            #print("Current Q-value: ", current_q_value)
            
            q_table[(current_state, action)] = current_q_value + ALPHA * (reward + GAMMA * max_next_q_value - current_q_value) 
            #print("Updated Q-value: ", q_table[(current_state, action)])
           
        # #print progress
        #if episode % 50 == 0:
            #print(f"Episode {episode + NUM_EPISODES} completed.")

    #print("Training complete!")
    save_q_table()
    save_episodes_num(num_episodes + NUM_EPISODES)

def calculate_convergence_of_algorithm():
    rewards_per_episode = []

    for episode in range(num_episodes + NUM_EPISODES):
        total_reward = 0
        dices = roll_dice()
        scoring_state = tuple([0] * 13)

        for turn in range(13):
            current_state = (tuple(dices), scoring_state)
            action = choose_action(current_state)
            reward = calculate_reward(dices, scoring_state, action)
            total_reward += reward

            new_scoring_state = list(scoring_state)
            if 0 <= action < len(new_scoring_state):
                new_scoring_state[action] = 1
            scoring_state = tuple(new_scoring_state)
            dices = roll_dice()
            new_state = (tuple(dices), scoring_state)

            max_next_q_value = max(
                q_table.get((new_state, act), 0.0) for act in range(13) if new_state[1][act] == 0
            )
            current_q_value = q_table.get((current_state, action), 0.0)
            q_table[(current_state, action)] = current_q_value + ALPHA * (
                reward + GAMMA * max_next_q_value - current_q_value
            )

        rewards_per_episode.append(total_reward)

    #Aplt.plot(range(num_episodes + NUM_EPISODES), rewards_per_episode)
    #Aplt.xlabel('Episode')
    #Aplt.ylabel('Total Reward')
    #Aplt.title('Convergence of Q-Learning Algorithm')
    #Aplt.show()

def AiMakesMoveHard(statePlayers):
    # Q-Learn strategy for the AI

    # THE DICE ROLLING PART
    statePlayers[2] = roll_dice()
    
    # THE CHOOSING PART BASED ON THE Q-LEARNING STRATEGY  

    # Making the section state like in the q-table
    new_state = [0 for _ in range(13)]
    ct = 0
    for i in statePlayers[3][:13]:
        if i == -1:
            new_state[ct] = 0
        elif i == 0:
            new_state[ct] = 0
        else:
            new_state[ct] = 1
        ct += 1

    # THE DICE CHOOSING PART ----------------------------
    for i in range(0, 2):
        #print("Ai choses the ", (i + 1), "th time")
        global EPSILON
        EPSILON = max(0.05, EPSILON - 0.05)
        if random.random() < EPSILON:
            #print("Random action")
            # Explore: Choose a random action
            statePlayers[2] = [i if random.random() <= EPSILON else 0 for i in statePlayers[2]]
            statePlayers[2] = [random.randint(1, 6) if i == 0 else i for i in statePlayers[2]]

            #print(new_state)

            action = random.choice([i for i in range(13) if new_state[i] == 0])
            continue
        
        # Dices like in the q-table
        dices = sorted(statePlayers[2])
        #print("Dices:", statePlayers[2])

        curent_state = tuple ((tuple(dices), tuple(new_state)))

        action = max(range(13), key=lambda action: q_table.get((curent_state, action), 0.0) if new_state[action] == 0 else 0.0)
        #for i in range(13):
            #print(q_table.get((curent_state, i), 0.0), end = " ")
        reward = q_table.get((curent_state, action), 0.0)
        #print("Action:", action)
        #print("Reward:", q_table.get((curent_state, action), 0.0))

        # Reroll the dices based on the action
        if action >= 0 and action <= 5:
            # reroll all dices diferit from 1
            statePlayers[2] = [statePlayers[2][i] if statePlayers[2][i] == (action + 1) else random.randint(1, 6) for i in range(5)] 
        elif action == 6:
            # 3 of a kind
            statePlayers[2] = [statePlayers[2][i] if statePlayers[2].count(statePlayers[2][i]) >= 3 else random.randint(1, 6) for i in range(5)]
        elif action == 7:
            # 4 of a kind
            statePlayers[2] = [statePlayers[2][i] if statePlayers[2].count(statePlayers[2][i]) >= 4 else random.randint(1, 6) for i in range(5)]
        elif action == 8:
            # Full House
            statePlayers[2] = [statePlayers[2][i] if statePlayers[2].count(statePlayers[2][i]) >= 2 else random.randint(1, 6) for i in range(5)]
        elif action == 9: 
            # Small Straight
            # keep only the dices that are in the small straight
            set_new_dices = set(statePlayers[2])
            dices = sorted(list(set_new_dices))

            dices14 = [i for i in dices if i <= 4 ]
            dices25 = [i for i in dices if i >= 2 and i <= 5]
            dices36 = [i for i in dices if i >= 3]

            if len(dices14) > len(dices25) and len(dices14) > len(dices36):
                statePlayers[2] = [statePlayers[2][i] if statePlayers[2][i] in dices14 else random.randint(1, 6) for i in range(5)]
            elif len(dices25) > len(dices14) and len(dices25) > len(dices36):
                statePlayers[2] = [statePlayers[2][i] if statePlayers[2][i] in dices25 else random.randint(1, 6) for i in range(5)]
            elif len(dices36) > len(dices14) and len(dices36) > len(dices25):
                statePlayers[2] = [statePlayers[2][i] if statePlayers[2][i] in dices36 else random.randint(1, 6) for i in range(5)]
            elif len(dices14) == len(dices25):
                statePlayers[2] = [statePlayers[2][i] if statePlayers[2][i] in dices14 or statePlayers[2][i] in dices25 else random.randint(1, 6) for i in range(5)]
            elif len(dices14) == len(dices36):
                statePlayers[2] = [statePlayers[2][i] if statePlayers[2][i] in dices25 else random.randint(1, 6) for i in range(5)]
            elif len(dices25) == len(dices36):
                statePlayers[2] = [statePlayers[2][i] if statePlayers[2][i] in dices25 or statePlayers[2][i] in dices36 else random.randint(1, 6) for i in range(5)]
            else:
                statePlayers[2] = [statePlayers[2][i] if statePlayers[2][i] in dices else random.randint(1, 6) for i in range(5)]

        elif action == 10:
            # Large Straight
            break # keep all of them 
        elif action == 11:
            # Yahtzee
            break # keep all of them
        elif action == 12:
            # Chance
            statePlayers[2] = [statePlayers[2][i] if statePlayers[2][i] > 3 else random.randint(1, 6) for i in range(5)]
        
        #print("AI chose to reroll")
        #print()
    # THE DICE CHOOSING PART ----------------------------

    alegere = max(range(13), key = lambda alegere: ScoreCalculation(statePlayers[2])[alegere] if statePlayers[3][alegere] == -1 else -1) 
    score = ScoreCalculation(statePlayers[2])[alegere]
    #print("Final dices:", statePlayers[2])
    #print("AI Player chose the section: ", sectionsForPlayers[alegere], " with score: ", score)

    statePlayers[3][alegere] = score
    statePlayers[3][13] = sum([i for i in statePlayers[3][0:6] if i != -1])
    statePlayers[3][14] = 35 if sum(statePlayers[3][0:6]) >= 63 else 0
    statePlayers[3][15] = sum([i for i in statePlayers[3][0:13] if i != -1]) + statePlayers[3][14]

    statePlayers[2] = reset_dice()
    statePlayers[1] = 4
    
    # RETURN THE STATE
    return statePlayers
