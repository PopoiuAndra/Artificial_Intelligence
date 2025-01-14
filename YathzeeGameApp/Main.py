from MediumDifficultAI import AiMakesMoveMedium
from EasyDifficultAI import  re, AiMakesMoveEasy, ScoreCalculation, IsFinalState, ShowScore
from HardDifficultAI import AiMakesMoveHard
import random
import pygame

AiMakesMove = None

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
        dices = list(map(int, re.findall(r'\d+', input())))
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

    # Player AI
    statePlayers[4] = [-1 if i <= 12 else 0 for i in range(13)]
    statePlayers[4].append(0)
    statePlayers[4].append(0)
    statePlayers[4].append(0)

def UpdatePlayerState(statePlayers):
    if IsFinalState(statePlayers):
        return None

    # Update the dices
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
        print()

        statePlayers[0] = 1
        statePlayers[1] = 0

    # Enters the next transition with the updated state
    UpdatePlayerState(statePlayers)

def main(): #game_assistant = initialize_assistant()
    global AiMakesMove
    print("Welcome to Medium Yahtzee! :)")
    print("Type 'help' during your turn to access the game assistant.")


# Initialize pygame
    pygame.init()

# Screen dimensions
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Yahtzee Game")

# Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)

# Fonts
    FONT = pygame.font.Font(None, 36)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #if a button is pr4essed
                if WIDTH//2 - 100 <= event.pos[0] <= WIDTH//2 + 100:
                    if HEIGHT//2 - 35 <= event.pos[1] <= HEIGHT//2 + 35:
                        print("Easy button pressed")
                        AiMakesMove = AiMakesMoveEasy
                        running = False
                    elif HEIGHT//2 + 55 <= event.pos[1] <= HEIGHT//2 + 125:
                        print("Medium button pressed")
                        AiMakesMove = AiMakesMoveMedium
                        running = False
                    elif HEIGHT//2 + 145 <= event.pos[1] <= HEIGHT//2 + 215:
                        print("Hard button pressed")
                        AiMakesMove = AiMakesMoveHard
                        running = False
                    else:
                        print("No button pressed")
                else:
                    print("No button pressed")
                print("Event pose : " , event.pos)
        # make the background DARK green
        screen.fill((0, 100, 0))

        # 3 buttons in the middle of the screen, one for east, one for medium and one for hard, at the top of the screen write choose difficulty
        # draw text
        text = FONT.render("Choose difficulty", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(text, text_rect)

        # draw buttons
        button_width, button_height = 200, 70
        button_x, button_y = WIDTH//2 - button_width//2, HEIGHT//2 - button_height//2
        pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
        text = FONT.render("Easy", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, text_rect)

        button_y += 90
        pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
        text = FONT.render("Medium", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + 90))
        screen.blit(text, text_rect)

        button_y += 90
        pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))
        text = FONT.render("Hard", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + 180))
        screen.blit(text, text_rect)

        pygame.display.flip()

    screen.fill(WHITE)
    pygame.display.flip()
    
    SetInitialState(statePlayers)
    
    while True:
        #if input().lower() == 'help':
            #await handle_assistance(game_assistant, statePlayers)
        
        UpdatePlayerState(statePlayers)
        
        if IsFinalState(statePlayers):
            break

# Initial 
sectionsForPlayers = ["One", "Two", "Three", "Four", "Five", "Six", "3 of a kind", "4 of a kind", "Full House", "Small Straight", "Large Straight", "Yahtzee", "Chance", "First 6 sections score", "Bonus", "Final Score"]
statePlayers = list(range(5))

main()