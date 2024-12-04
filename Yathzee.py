import random
from itertools import product
import os
import pickle
import matplotlib.pyplot as plt

# Constants
num_episodes = 10000
NUM_EPISODES = 0
ALPHA = 0.9  # Learning rate
GAMMA = 0.9  # Discount factor
EPSILON = 0.1  # Exploration rate
Q_TABLE_FILE = 'q_table.pkl'  # File in which the Q-table will be saved
Q_NUM_FILE = 'num_episodes.pkl' # File in which the number of episodes will be saved

# Generate all possible dice configurations
dice_configurations = sorted(set(''.join(map(str, sorted(dice))) for dice in product(range(1, 7), repeat=5)))
print(F"Number of possible dices combinations: {len(dice_configurations)}")

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
    print(type(q_table))
else:
    q_table = {}
    NUM_EPISODES = NUM_EPISODES

def save_q_table():
    with open(Q_TABLE_FILE, 'wb') as f:
        pickle.dump(q_table, f)
        
def save_episodes_num(num_episodes):
    with open(Q_NUM_FILE, "wb") as f:
        pickle.dump(num_episodes, f)

def choose_action(state):
    if random.random() < EPSILON:
        #print("Random action")
        # Explore: Choose a random action
        # EPSILON = max(0.1, EPSILON - 0.001) ---------------------------------IDK IF IT IS NEEDED
        return random.choice([i for i in range(0,13) if state[1][i] == 0])
    else:
        #print("Best action")
        # Exploit: Choose the best-known action
        return max(range(len(state[1])), 
               key=lambda action: q_table.get((state, action), 0.0))
         #A ce inseamna actionul ca are valori gigantice
        #return max(range(13), key = lambda action: calculate_reward(state[0], state[1], action) )

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

def train_q_learning():  #------------STARTED NOT FINISHED-----TO BE ADAPTED COMPLETELY TO OUR CODE---------------
    for episode in range(num_episodes):
        # Initialize the game state
        dices = roll_dice()
        scoring_state = tuple([0] * 13)  # All categories initially empty
        #print(scoring_state)
        #SetInitialState(statePlayers)

        for turn in range(13):  # Maximum of 13 turns per game/episode
            # Define the current state
            current_state = (tuple(dices), scoring_state)
            #print("Current state: ", current_state)

            # Choose an action (scoring category) using epsilon-greedy policy
            action = choose_action(current_state)
            #print("Action: ", action)

            # Calculate the reward for the chosen action
            reward = calculate_reward(dices, scoring_state, action)
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
            #print("new Dices: ", dices)

            # Define the new state
            new_state = (tuple(dices), scoring_state)

            # Compute the maximum Q-value for the next state
            max_next_q_value = max(
                q_table.get((new_state, act), 0.0) for act in range(13) if new_state[1][act] == 0
            )
            #print("Max next Q-value: ", max_next_q_value)

            # Update Q-value using the Q-learning formula
            current_q_value = q_table.get((current_state, action), 0.0) #A sum(dices))? 
            #print("Current Q-value: ", current_q_value)
            #A nu trebuia sa fie current_q_value = q_table.get((dices, current_state), 0.0)? + ce e 0.0?
            q_table[(current_state, action)] = current_q_value + ALPHA * (
                reward + GAMMA * max_next_q_value - current_q_value
            )
            #print("Updated Q-value: ", q_table[(current_state, action)])
            #A scoring_state trebuie updatat - nu stiu daca nu scumva e printr o functie da nu cred
        # Optional: Print progress
        if episode % 50 == 0:
            print(f"Episode {episode + NUM_EPISODES} completed.")

    print("Training complete!")
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

    plt.plot(range(num_episodes + NUM_EPISODES), rewards_per_episode)
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.title('Convergence of Q-Learning Algorithm')
    plt.show()

def ShowScore(statePlayers):
    print()
    print("Player 1 - Total score: " + str(statePlayers[3][13]) + " Bonus: " + str(statePlayers[3][14]) + " Final score: " + str(statePlayers[3][15]))
    print("Player 2 - Total score: " + str(statePlayers[4][13]) + " Bonus: " + str(statePlayers[4][14]) + " Final score: " + str(statePlayers[4][15]))

    print("THE WINNER IS ", "PLAYER 1!" if statePlayers[3][15] > statePlayers[4][15] else "PLAYER 2!")

def IsFinalState(statePlayers):
    if -1 not in statePlayers[3][:13] and -1 not in statePlayers[4][:13]:
        # Show the score table 
        ShowScore(statePlayers) 
        # Is final state
        return True
    else:
        # Is not final state
        return False 
        # Continue game normaly

def ScoreCalculation(dices):
    # Firts 6 sections, 3 of a kind, 4 of a kind, Yahtzee
    score = [0 for _ in range(16)]
    for i in range(1, 7):
        score[i - 1] = dices.count(i) * i
        if dices.count(i) == 3:
            score[6] = sum(dices)
        if dices.count(i) == 4:
            score[7] = sum(dices)
        if dices.count(i) == 5:
            score[11] = 50 # Yahtzee
        
    # Small Straight | Large Straight
    if 3 in dices and 4 in dices:
        # Has chance to be small straight or large straight
        if 2 in dices and 5 in dices:
            if 1 not in dices and 6 not in dices:
                score[9] = 30
            else:
                score[9] = 30
                score[10] = 40
        if 1 in dices and 2 in dices:
            if 5 not in dices:
                score[9] = 30
            else:
                score[9] = 30
                score[10] = 40
        if 5 in dices and 6 in dices:
            if 2 not in dices:
                score[9] = 30
            else:
                score[9] = 30
                score[10] = 40
        
    # Full House
    for i in range(1, 7):
        if dices.count(i) == 3:
            for j in range(1, 7):
                if dices.count(j) == 2 and i != j:
                    score[8] = 25
                    break

    # Chance
    score[12] = sum(dices)

    return score

def AiMakesMove(statePlayers):
    # Q-Learn strategy for the AI

    # THE DICE ROLLING PART
    statePlayers[2] = roll_dice()
    
    print("Dices: " + str(statePlayers[2]))
    
    # THE CHOOSING PART BASED ON THE Q-LEARNING STRATEGY      ----------------TO BE DONE----------------
    #A print(q_table((statePlayers[2], statePlayers[3])))
    # # print("Scores: " + str(score))
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

    print("StatePlayers[2]:", statePlayers[2], "Type:", type(statePlayers[2]))
    print("StatePlayers[3]:", new_state, "Type:", type(new_state))
    curent_state = tuple ((tuple(statePlayers[2]), tuple(new_state)))
    for action in range(13):
        print("Action:", action)
        print(q_table.get( ( curent_state, action), -1.0))

    action = max(range(13), key=lambda action: q_table.get((curent_state, action), 0.0))
    print("Action:", action)
    print("Reward:", q_table.get((curent_state, action), 0.0))

    # for i in range(0, 3):
    #     actiune = 0 # o actuine
    #     if actiune == 0: # daca da reroll
    #         # alege cum face reroll
    #         print("HEi ;)")
    #     else:
    #         break
    # alegere = 0 #A o sa fie altceva aici probabil fin for
    # score = calculate_reward(statePlayers[2], statePlayers[3], 0)

    # statePlayers[3][alegere] = score
    # statePlayers[3][13] = sum([i for i in statePlayers[3][0:6] if i != -1])
    # statePlayers[3][14] = 35 if sum(statePlayers[3][0:6]) >= 63 else 0
    # statePlayers[3][15] = sum([i for i in statePlayers[3][0:13] if i != -1]) + statePlayers[3][14]


    # # The player can choose only one section
    # chosen_section = -1
    # available_sections = [i for i in range(0, 13) if statePlayers[3][i] == -1 and score[i] != 0]
    # if len(available_sections) == 0: # No available sections
    #     print("All sections are full, choosing a random section.")
        
    #     sections = [i for i in range(0, 13) if statePlayers[3][i] == -1]
    #     print("Sections: ", sections)

    #     chosen_section = random.choice(sections)
    #     statePlayers[3][chosen_section] = 0
    # else:
    #     chosen_section = random.choice(available_sections)
    #     statePlayers[3][chosen_section] = score[chosen_section]
    #     # sum
    #     statePlayers[3][13] = sum([i for i in statePlayers[3][0:6] if i != -1])
    #     # bonus
    #     statePlayers[3][14] = 35 if sum(statePlayers[3][0:6]) >= 63 else 0
    #     # total score
    #     statePlayers[3][15] = sum([i for i in statePlayers[3][0:13] if i != -1]) + statePlayers[3][14]
    #     # print("Player AI state: " + str(statePlayers[3]))
    
    # print("AI Player chose the section " + sectionsForPlayers[chosen_section] + " with score: " + str(score[chosen_section]))

    # THE SECTION CHOOSING PART ----------------------------

    # SETING THE DICES TO THE LAST ARRANGEMENT
    statePlayers[2] = reset_dice()
    statePlayers[1] = 4
    
    # RETURN THE STATE
    return statePlayers

def UserMakesMove(statePlayers):
    
    # THE DICE CHOOSING PART ----------------------------
    statePlayers[1] += 1

    source = []
    print("Your dices: \n 0  1  2  3  4" + "\n" + str(statePlayers[2]))
    if statePlayers[1] == 3:
        source = statePlayers[2]
        print("You have reached the maximum number of throws.")
    else:
        print("Choose the dices that you want to keep(the index number): ")
        dices = list(map(int, input().split()))
        for i in range(0,5):
            if i in dices:
                source.append(statePlayers[2][i])
            else:
                source.append(0)
    
    statePlayers[2] = source
    # print("Player 2 chosen dices: " + str(statePlayers[2]))

    if source.count(0) != 0:
        # It moves to the next state
        return statePlayers
    else :
        statePlayers[1] = 4
    
    # THE DICE CHOOSING PART ----------------------------

    # THE SECTION CHOOSING PART ----------------------------
    # Seing if the section is available

    # first 6 sections and the 3 of a kind, 4 of a kind and yetzee sections can be chosen 
    score = ScoreCalculation(statePlayers[2])

    # print("Player 2 state before: " + str(statePlayers[4]))

    score = [0 if statePlayers[4][i] != -1 else score[i] for i in range(0, 13)]
    if sum(score) == 0:
        print("All sections are full, choose an available section to score 0.")
        for i in range(14):
            if statePlayers[4][i] == -1:
                print("index: ", i, " ",  sectionsForPlayers[i])
        
        valid_choice = False
        while valid_choice == False:
            print("Choose the section: ")
            chosen_section = int(input())
            if chosen_section >= 0 and chosen_section <= 12 and statePlayers[4][chosen_section] == -1:
                valid_choice = True
                statePlayers[4][chosen_section] = 0
            else: print("Choose a valid section:")

        
        statePlayers[4][13] = sum([i for i in statePlayers[4][0:6] if i != -1])
        statePlayers[4][14] = 35 if sum(statePlayers[4][0:6]) >= 63 else -1
        statePlayers[4][15] = sum([i for i in statePlayers[4][0:13] if i != -1]) + statePlayers[4][14]
        return statePlayers
    
    print("The available sections: ")
    for i in range(0, 13):
        if statePlayers[4][i] == -1 and score[i] != 0:
            print("index: ", i, " ",  sectionsForPlayers[i], " score: ", score[i])
    
    valid_choice = False
    while valid_choice == False:
        print("Choose the section: ")
        chosen_section = int(input())
        if chosen_section >= 0 and chosen_section <= 12 and statePlayers[4][chosen_section] == -1 and score[chosen_section] != 0:
            valid_choice = True
            statePlayers[4][chosen_section] = score[chosen_section]
        else:
            print("Choose a valid section:")
    
    statePlayers[4][13] = sum([i for i in statePlayers[4][0:6] if i != -1])
    statePlayers[4][14] = 35 if sum(statePlayers[4][0:6]) >= 63 else 0
    statePlayers[4][15] = sum([i for i in statePlayers[4][0:13] if i != -1]) + statePlayers[4][14]

    # print("Player 2 state: " + str(statePlayers))

    statePlayers[1] = 4
    statePlayers[2] = [0, 0, 0, 0, 0]
    return statePlayers

def UpdatePlayerState(statePlayers):
    # print("IN UPDATE PLAYER STATE")
    if IsFinalState(statePlayers):
        return None

    # Update the dices
    # print("Player dices before: " + str(statePlayers[2]))
    statePlayers[2] = [random.randint(1, 6) if x == 0 else x for x in statePlayers[2]]

    # Player AI turn
    if statePlayers[0] == 1 and statePlayers[1] <= 3:
        AiMakesMove(statePlayers)
    elif statePlayers[0] == 1:
        # The turn changes
        print()
        print("YOUR TURN")

        print()
        print("Players state:")
        print("\t AI Player: " + str([i if i != -1 else '-' for i in statePlayers[3][0:13]]), " First 6 sections score: ", statePlayers[3][13], " Bonus: ", statePlayers[3][14], " Total score: ", statePlayers[3][15])
        print("\t You      : " + str([i if i != -1 else '-' for i in statePlayers[4][0:13]]), " First 6 sections score: ", statePlayers[4][13], " Bonus: ", statePlayers[4][14], " Total score: ", statePlayers[4][15])
        print()

        statePlayers[0] = 2
        statePlayers[1] = 0

    # Phisical player turn
    elif statePlayers[0] == 2 and statePlayers[1] <= 3:
        UserMakesMove(statePlayers)
    elif statePlayers[0] == 2:
        # The turn changes
        print()
        print("AI PLAYER TURN")

        statePlayers[0] = 1
        statePlayers[1] = 0

    # Enters the next transition with the updated state
    UpdatePlayerState(statePlayers)
        
def SetInitialState(statePlayers):
    # The Player AI starts
    statePlayers[0] = 1

    # The Player AI has not rolled the dices yet
    statePlayers[1] = 0

    # The dices are not rolled yet
    statePlayers[2] =  [0, 0, 0, 0, 0]
    
    # Player 1
    statePlayers[3] = [-1 if i <= 12 else 0 for i in range(13)]
    statePlayers[3].append(0) # First 6 sections score
    statePlayers[3].append(0) # Bonus
    statePlayers[3].append(0) # Total score

    # Player 2
    statePlayers[4] = [-1 if i <= 12 else 0 for i in range(13)]
    statePlayers[4].append(0)
    statePlayers[4].append(0)
    statePlayers[4].append(0)


# MAIN LIKE FUNCTION

# After training is done, you can play the game 
sectionsForPlayers = ["One", "Two", "Three", "Four", "Five", "Six", "3 of a kind", "4 of a kind", "Full House", "Small Straight", "Large Straight", "Yahtzee", "Chance", "First 6 sections score", "Bonus", "Final Score"]
statePlayers = list(range(5))

# Call the function to start training
train_q_learning()

calculate_convergence_of_algorithm()

print("Welcome to Yahtzee! :)")
print()
SetInitialState(statePlayers)

UpdatePlayerState(statePlayers)