import random

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
    # Random strategy for the AI

    # THE DICE CHOOSING PART ----------------------------
    # print("Player AI dices: " + str(statePlayers[2]))

    # Chose the dices that will be used
    # The AI player can chose the dices that he wants to keep (first throw)
    statePlayers[2] = [i if random.randint(0, 1) == 1 else 0 for i in statePlayers[2]]
    # print("Player AI chosen dices: " + str(statePlayers[2]))
    
    # The AI player can chose more dices (second throw)
    # The new dices are added
    statePlayers[2] = [random.randint(1, 6) if i == 0 else i for i in statePlayers[2]]
    # print("Player AI new dices: " + str(statePlayers[2]))

    # The AI player can chose the section
    statePlayers[2] = [i if random.randint(0, 1) == 1 else 0 for i in statePlayers[2]]
    # print("Player AI chosen section: " + str(statePlayers[2]))

    # The AI player can choose more dices (third throw)
    # The new dices are added
    statePlayers[2] = [random.randint(1, 6) if i == 0 else i for i in statePlayers[2]]
    print("AI Player Dices: " + str(statePlayers[2]))

    # The AI player is stuck with the dices that he choose
    # THE DICE CHOOSING PART ----------------------------
    
    # THE SECTION CHOOSING PART ----------------------------
    score = ScoreCalculation(statePlayers[2])
    # print("Scores: " + str(score))

    # The player can choose only one section
    chosen_section = -1
    available_sections = [i for i in range(0, 13) if statePlayers[3][i] == -1 and score[i] != 0]
    if len(available_sections) == 0: # No available sections
        print("All sections are full, choosing a random section.")
        
        sections = [i for i in range(0, 13) if statePlayers[3][i] == -1]
        print("Sections: ", sections)

        chosen_section = random.choice(sections)
        statePlayers[3][chosen_section] = 0
    else:
        chosen_section = random.choice(available_sections)
        statePlayers[3][chosen_section] = score[chosen_section]
        # sum
        statePlayers[3][13] = sum([i for i in statePlayers[3][0:6] if i != -1])
        # bonus
        statePlayers[3][14] = 35 if sum(statePlayers[3][0:6]) >= 63 else 0
        # total score
        statePlayers[3][15] = sum([i for i in statePlayers[3][0:13] if i != -1]) + statePlayers[3][14]
        # print("Player AI state: " + str(statePlayers[3]))
    
    print("AI Player chose the section " + sectionsForPlayers[chosen_section] + " with score: " + str(score[chosen_section]))

    # THE SECTION CHOOSING PART ----------------------------

    # SETING THE DICES TO THE LAST ARRANGEMENT
    statePlayers[1] = 4
    statePlayers[2] = [0, 0, 0, 0, 0]
    
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

# MAIN LIKE 
# Initial Configuration
sectionsForPlayers = ["One", "Two", "Three", "Four", "Five", "Six", "3 of a kind", "4 of a kind", "Full House", "Small Straight", "Large Straight", "Yahtzee", "Chance", "First 6 sections score", "Bonus", "Final Score"]
statePlayers = list(range(5))

print("Welcome to Yahtzee! :)")
print()
SetInitialState(statePlayers)

UpdatePlayerState(statePlayers)
