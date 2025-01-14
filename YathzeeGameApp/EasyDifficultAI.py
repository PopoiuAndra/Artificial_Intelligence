import random
import re

# Initial Configuration
sectionsForPlayers = ["One", "Two", "Three", "Four", "Five", "Six", "3 of a kind", "4 of a kind", "Full House", "Small Straight", "Large Straight", "Yahtzee", "Chance", "First 6 sections score", "Bonus", "Final Score"]

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

def AiMakesMoveEasy(statePlayers):
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
