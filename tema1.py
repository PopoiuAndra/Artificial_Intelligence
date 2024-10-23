import random

# TO BE DONE
def ShowScore(statePlayers):
    print("Player 1: Total score: " + str(statePlayers[3][13]) + " Bonus: " + str(statePlayers[3][14]) + " Final score: " + str(statePlayers[3][15]))
    print("Player 2: Total score: " + str(statePlayers[4][13]) + " Bonus: " + str(statePlayers[4][14]) + " Final score: " + str(statePlayers[4][15]))

def IsFinalState(statePlayers):
    if -1 not in statePlayers[3] and -1 not in statePlayers[4]:
        # Show the score table 
        ShowScore(statePlayers) 
        # Is final state
        return True
    else:
        # Is not final state
        return False 
        # Continue game normaly

# GOOD I THINK? TO BE DONE 
def AiMakesMove(statePlayers):
    
    # Random strategy for the AI

    # THE DICE CHOOSING PART ----------------------------
    # print("Player AI dices: " + str(statePlayers[2]))

    # Chose the dices that will be used
    statePlayers[2] = [i if random.randint(0, 1) == 1 else 0 for i in statePlayers[2]]
    # print("Player AI chosen dices: " + str(statePlayers[2]))
    
    # The player can chose more dices (second throw)

    # The new dices are added
    statePlayers[2] = [random.randint(1, 6) if i == 0 else i for i in statePlayers[2]]
    # print("Player AI new dices: " + str(statePlayers[2]))

    # The player can chose the section
    statePlayers[2] = [i if random.randint(0, 1) == 1 else 0 for i in statePlayers[2]]
    # print("Player AI chosen section: " + str(statePlayers[2]))

    # The player can choose more dices (third throw)

    # The new dices are added
    statePlayers[2] = [random.randint(1, 6) if i == 0 else i for i in statePlayers[2]]
    print("Player AI new dices: " + str(statePlayers[2]))

    # The player is stuck with the dices that he choose
    # THE DICE CHOOSING PART ----------------------------
    
    # THE SECTION CHOOSING PART ----------------------------
    # Seing if the section is available

    # first 6 sections and the 3 of a kind, 4 of a kind and yetzee sections can be chosen 
    score = [0 for _ in range(16)]
    for i in range(1, 7):
        score[i - 1] = statePlayers[2].count(i) * i
        if statePlayers[2].count(i) == 3:
            score[6] = sum(statePlayers[2])
        if statePlayers[2].count(i) == 4:
            score[7] = sum(statePlayers[2])
        if statePlayers[2].count(i) == 5:
            score[11] = 50 # Yahtzee
        
    # Small Straight | Large Straight
    if 3 in statePlayers[2] and 4 in statePlayers[2]:
        # Has chance to be small straight or large straight
        if 2 in statePlayers[2] and 5 in statePlayers[2]:
            if 1 not in statePlayers[2] and 6 not in statePlayers[2]:
                score[9] = 30
            else:
                score[9] = 30
                score[10] = 40
        if 1 in statePlayers[2] and 2 in statePlayers[2]:
            if 5 not in statePlayers[2]:
                score[9] = 30
            else:
                score[9] = 30
                score[10] = 40
        if 5 in statePlayers[2] and 6 in statePlayers[2]:
            if 2 not in statePlayers[2]:
                score[9] = 30
            else:
                score[9] = 30
                score[10] = 40
        
    # Full House
    for i in range(1, 7):
        if statePlayers[2].count(i) == 3:
            for j in range(1, 7):
                if statePlayers[2].count(j) == 2 and i != j:
                    score[8] = 25

    # Chance
    score[12] = sum(statePlayers[2])

    print("Scores: " + str(score))

    # The player can choose only one section
    chosen_section = -1
    available_sections = [i for i in range(0, 13) if statePlayers[3][i] == -1 and score[i] != 0]
    if len(available_sections) == 0:
        print("All sections are full, choosing a random section.")
        # SOMETHING HERE IS WRONG
        sections = [i for i in range(0, 13) if statePlayers[3][i] == -1]
        print("Sections: ", sections)
        chosen_section = random.choice(sections)
        statePlayers[3][chosen_section] = 0
    else:
        chosen_section = random.choice(available_sections)
        statePlayers[3][chosen_section] = score[chosen_section]
        statePlayers[3][13] = sum([i for i in statePlayers[3][0:13] if i != -1])
        statePlayers[3][14] = 35 if sum(statePlayers[3][0:6]) >= 63 else 0
        print("Player AI state: " + str(statePlayers[3]))
    
    print("Player AI chosen section: " + sectionsForPlayers[chosen_section] + " with score: " + str(score[chosen_section]))

    # THE SECTION CHOOSING PART ----------------------------

    # SETING THE DICES  TO THE LAST ARRANGEMENT
    statePlayers[1] = 4
    statePlayers[2] = [0, 0, 0, 0, 0]
    
    # Return the state
    return statePlayers

# TO BE DONE 
def UserMakesMove(statePlayers):
    
    # THE DICE CHOOSING PART ----------------------------
    statePlayers[1] += 1

    source = []
    print("Player 2 dices: \n 0  1  2  3  4" + "\n" + str(statePlayers[2]))
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
    print("Player 2 chosen dices: " + str(statePlayers[2]))

    if source.count(0) != 0:
        # It moves to the next state
        return statePlayers
    
    else :
        statePlayers[1] = 4
    
    # THE DICE CHOOSING PART ----------------------------

    # THE SECTION CHOOSING PART ----------------------------
    # Seing if the section is available

    # first 4 sections and the 3 of a kind, 4 of a kind and yetzee sections can be chosen 
    score = [0 for _ in range(16)]
    for i in range(1, 7):
        score[i - 1] = statePlayers[2].count(i) * i
        if statePlayers[2].count(i) == 3:
            score[6] = sum(statePlayers[2])
        if statePlayers[2].count(i) == 4:
            score[7] = sum(statePlayers[2])
        if statePlayers[2].count(i) == 5:
            score[11] = 50 # Yahtzee
        
    # Small Straight | Large Straight
    if 3 in statePlayers[2] and 4 in statePlayers[2]:
        # Has chance to be small straight or large straight
        if 2 in statePlayers[2] and 5 in statePlayers[2]:
            if 1 not in statePlayers[2] and 6 not in statePlayers[2]:
                score[9] = 30
            else:
                score[9] = 30
                score[10] = 40
        if 1 in statePlayers[2] and 2 in statePlayers[2]:
            if 5 not in statePlayers[2]:
                score[9] = 30
            else:
                score[9] = 30
                score[10] = 40
        if 5 in statePlayers[2] and 6 in statePlayers[2]:
            if 2 not in statePlayers[2]:
                score[9] = 30
            else:
                score[9] = 30
                score[10] = 40
        
    # Full House
    for i in range(1, 7):
        if statePlayers[2].count(i) == 3:
            for j in range(1, 7):
                if statePlayers[2].count(j) == 2 and i != j:
                    score[8] = 25

    # Chance
    score[12] = sum(statePlayers[2])

    print("Player 2 state before: " + str(statePlayers[4]))

    score = [0 if statePlayers[4][i] != -1 else score[i] for i in range(0, 13)]
    if sum(score) == 0:
        print("All sections are full, choose an available section to score 0.")
        for i in range(14):
            if statePlayers[4][i] == -1:
                print("index: ", i, " ",  sectionsForPlayers[i])

        print("Choose the section: ")
        chosen_section = int(input())
        statePlayers[4][chosen_section] = 0

        statePlayers[4][13] = sum([i for i in statePlayers[4][0:13] if i != -1])
        statePlayers[4][14] = 35 if sum(statePlayers[4][0:6]) >= 63 else 0
        return statePlayers
    
    print("Choose the section: ")
    for i in range(0, 13):
        if statePlayers[4][i] == -1 and score[i] != 0:
            print("index: ", i, " ",  sectionsForPlayers[i], " score: ", score[i])
    print("Choose the section: ")
    chosen_section = int(input())
    statePlayers[4][chosen_section] = score[chosen_section]
    
    statePlayers[4][13] = sum([i for i in statePlayers[4][0:13] if i != -1])
    statePlayers[4][14] = 35 if sum(statePlayers[4][0:6]) >= 63 else -1

    print("Player 2 state: " + str(statePlayers))

    statePlayers[2] = [0, 0, 0, 0, 0]
    return statePlayers

def UpdatePlayerState(statePlayers):
    print("IN UPDATE PLAYER STATE")
    if IsFinalState(statePlayers):
        return None
    
    print("Player 1: " + str(statePlayers[3]))
    print("Player 2: " + str(statePlayers[4]))

    # Update the dices
    print("Player dices before: " + str(statePlayers[2]))
    statePlayers[2] = [random.randint(1, 6) if x == 0 else x for x in statePlayers[2]]

    # Player AI turn
    if statePlayers[0] == 1 and statePlayers[1] <= 3:
        AiMakesMove(statePlayers)
    elif statePlayers[0] == 1:
        # The turn changes
        statePlayers[0] = 2
        statePlayers[1] = 0
    elif statePlayers[0] == 2 and statePlayers[1] <= 3:
        UserMakesMove(statePlayers)
    elif statePlayers[0] == 2:
        # The turn changes
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
    statePlayers[3].append(0)
    statePlayers[3].append(0)
    statePlayers[3].append(0)

    # Player 2
    statePlayers[4] = [-1 if i <= 12 else 0 for i in range(13)]
    statePlayers[4].append(0)
    statePlayers[4].append(0)
    statePlayers[4].append(0)

# MAIN LIKE 

# Initial Configuration
sectionsForPlayers = ["One", "Two", "Three", "Four", "Five", "Six", "3 of a kind", "4 of a kind", "Full House", "Small Straight", "Large Straight", "Yahtzee", "Chance", "Total", "Bonus", "Final Score"]
statePlayers = list(range(5))
SetInitialState(statePlayers)
print("Initial state: \n" + str(statePlayers)) 

print([i for i in range(0,5)])

# Start the game
# statePlayers[3] = [0, 0, 0, 4, 10, 0, 15, -1, 0, -1, -1, -1, 14, 43, 0, 0]
UpdatePlayerState(statePlayers)
print("State after the first move: \n" + str(statePlayers))

print(ShowScore(statePlayers))



#UserMakesMove(statePlayers)