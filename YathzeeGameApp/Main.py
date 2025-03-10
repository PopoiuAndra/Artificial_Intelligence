from MediumDifficultAI import AiMakesMoveMedium, minimax
from EasyDifficultAI import  re, AiMakesMoveEasy, ScoreCalculation
from HardDifficultAI import AiMakesMoveHard, q_table, train_q_learning
from OllamaAssistant import ask_about_yahtzee
import random
import pygame

AiMakesMove = None

def ShowScore(statePlayers):
    global restart_game, decision_vector
    print()
    # calcul the bonus for player 1 and ai player
    statePlayers[3][13] = sum([i for i in statePlayers[3][0:6] if i != -1])
    statePlayers[3][14] = 35 if sum(statePlayers[3][0:6]) >= 63 else 0
    statePlayers[3][15] = sum([i for i in statePlayers[3][0:13] if i != -1]) + statePlayers[3][14]

    statePlayers[4][13] = sum([i for i in statePlayers[4][0:6] if i != -1])
    statePlayers[4][14] = 35 if sum(statePlayers[4][0:6]) >= 63 else 0
    statePlayers[4][15] = sum([i for i in statePlayers[4][0:13] if i != -1]) + statePlayers[4][14]

    print("Player 1 - Total score: " + str(statePlayers[3][13]) + " Bonus: " + str(statePlayers[3][14]) + " Final score: " + str(statePlayers[3][15]))
    print("Player 2 - Total score: " + str(statePlayers[4][13]) + " Bonus: " + str(statePlayers[4][14]) + " Final score: " + str(statePlayers[4][15]))

    print("THE WINNER IS ", "PLAYER 1!" if statePlayers[3][15] > statePlayers[4][15] else "PLAYER 2!")
    restart_game = False
    while restart_game == False:    
        draw_end(screen, statePlayers, generate_decision_feedback(decision_vector))

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

def UserMakesMove(statePlayers):
    global choose_button, row_chosen, can_choose_section, selected_dice, decision_vector, round
    selected_dice = [False] * NUM_DICE
    can_choose_section = [0 for _ in range(13)]
    
    # THE DICE CHOOSING PART ----------------------------
    statePlayers[1] += 1

    source = []
    dices = statePlayers[2]
    print("Your dices: \n 0  1  2  3  4" + "\n" + str(statePlayers[2]))
    if statePlayers[1] == 3:
        round += 1
        source = statePlayers[2]
        print("You have reached the maximum number of throws.")
    else:
        print("Choose the dices that you want to keep(the index number): ")
        choose_button = False
        dices = []
        while choose_button == False: ## ramane blocat in whileul asta
            source = draw_screen(screen, statePlayers)
        print("Finished choosing the dices.")
        for i in range(0,5):
            if i in source:
                dices.append(statePlayers[2][i])
            else:
                dices.append(0)
        print("Your chosen dices: " + str(source))
        new_vec = [0 if i == -1 else 1 for i in statePlayers[4]]
        print("Decision ", decide_dice_to_keep(statePlayers[2], new_vec))
        decision_vector.append((round, statePlayers[1], source, decide_dice_to_keep(statePlayers[2],  new_vec), statePlayers[2]))
        print("Decision vector: ", generate_decision_feedback(decision_vector))

    
    statePlayers[2] = dices
    # print("Player 2 chosen dices: " + str(statePlayers[2]))

    if dices.count(0) != 0:
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
        print("All sections are full, choose an available section to score 0.") ## there is a problem here -> can_choose_section is not updated??
        for i in range(13):
            if statePlayers[4][i] == -1:
                can_choose_section[i] = 1
                print("index: ", i, " ",  sectionsForPlayers[i])
        
        print([i for i in can_choose_section])
        
        valid_choice = False
        while valid_choice == False:
            print("Choose the section: ")
            print("before while")
            row_chosen = False
            row = -1
            while row_chosen == False:
                row = draw_screen(screen, statePlayers)
                if row != None: print("row: ", row)
                if row_chosen == True and statePlayers[4][row] == -1:
                    row_chosen = True
                    valid_choice = True
                    statePlayers[4][row] = score[row]
                else : row_chosen = False
            print("after while ", row)

        
        statePlayers[4][13] = sum([i for i in statePlayers[4][0:6] if i != -1])
        statePlayers[4][14] = 35 if sum(statePlayers[4][0:6]) >= 63 else -1
        statePlayers[4][15] = sum([i for i in statePlayers[4][0:13] if i != -1]) + statePlayers[4][14]
        return statePlayers
    
    print("The available sections: ")
    for i in range(0, 13):
        if statePlayers[4][i] == -1 and score[i] != 0:
            can_choose_section[i] = 1
            print("index: ", i, " ",  sectionsForPlayers[i], " score: ", score[i])
    
    print([i for i in can_choose_section])

    valid_choice = False
    while valid_choice == False:
        print("Choose the section: ")
        print("before while")
        row_chosen = False
        row = -1
        while row_chosen == False:
            row = draw_screen(screen, statePlayers)
            if row != None: print("row: ", row)
            if row_chosen == True and statePlayers[4][row] == -1 and score[row] != 0:
                row_chosen = True
                valid_choice = True
                statePlayers[4][row] = score[row]
            else : row_chosen = False
        print("after while ", row)
    
    statePlayers[4][13] = sum([i for i in statePlayers[4][0:6] if i != -1])
    statePlayers[4][14] = 35 if sum(statePlayers[4][0:6]) >= 63 else 0
    statePlayers[4][15] = sum([i for i in statePlayers[4][0:13] if i != -1]) + statePlayers[4][14]

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
    draw_screen(screen, statePlayers)
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

def draw_dice():
    """Draw dice and their outlines."""
    for i in range(NUM_DICE):
        x = DICE_X_START + i * (DICE_SIZE + DICE_MARGIN)
        y = DICE_Y
        # Draw dice background
        pygame.draw.rect(screen, GRAY, (x, y, DICE_SIZE, DICE_SIZE))
        
        value_text = FONT.render(str(statePlayers[2][i]), True, BLACK)
        text_rect = value_text.get_rect(center=(x + DICE_SIZE // 2, y + DICE_SIZE // 2))
        screen.blit(value_text, text_rect)
        # Draw outline
        outline_color = ORANGE if selected_dice[i] else BLACK
        pygame.draw.rect(screen, outline_color, (x, y, DICE_SIZE, DICE_SIZE), 3)

def draw_choose_button():
    """Draw the 'Choose' button."""
    pygame.draw.rect(screen, LIGHT_GREEN, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, BLACK, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT), 3)
    button_text = FONT.render("Reroll", True, BLACK)
    text_rect = button_text.get_rect(center=(BUTTON_X + BUTTON_WIDTH // 2, BUTTON_Y + BUTTON_HEIGHT // 2))
    screen.blit(button_text, text_rect)

def toggle_dice_selection(mouse_pos):
    """Toggle the selection of a dice based on the mouse position."""
    for i in range(NUM_DICE):
        x = DICE_X_START + i * (DICE_SIZE + DICE_MARGIN)
        y = DICE_Y
        dice_rect = pygame.Rect(x, y, DICE_SIZE, DICE_SIZE)
        if dice_rect.collidepoint(mouse_pos):
            selected_dice[i] = not selected_dice[i]

def is_choose_button_clicked(mouse_pos):
    """Check if the 'Choose' button is clicked."""
    button_rect = pygame.Rect(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)
    return button_rect.collidepoint(mouse_pos)

def draw_help_screen(screen, statePlayers): 
    global go_back, chat_history, text_input
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Typing into the text box
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # "Ask" the question when Enter is pressed
                if text_input.strip():
                    chat_history.append(("You", text_input.strip()))
                    if text_input.strip() == "next":
                        answer = "A good next move would be to choose " + str(decide_dice_to_keep(statePlayers[2], [0 if i == -1 else 1 for i in statePlayers[4]]))
                    else : answer = ask_about_yahtzee(text_input.strip())
                    chat_history.append(("Bot", answer))
                    text_input = ""  # Reset input
            elif event.key == pygame.K_BACKSPACE:
                text_input = text_input[:-1]  # Remove last character
            else:
                text_input += event.unicode  # Add typed character

        # Clicking the "Ask" button
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            ask_button_rect = pygame.Rect(
                WIDTH - 100 - MARGIN, HEIGHT - TEXT_BOX_HEIGHT - MARGIN, 100, TEXT_BOX_HEIGHT
            )
            if ask_button_rect.collidepoint(mouse_x, mouse_y):
                if text_input.strip():
                    chat_history.append(("You", text_input.strip()))
                    if text_input.strip() == "next":
                        answer = "A good next move would be to choose " + str(decide_dice_to_keep(statePlayers[2], [0 if i == -1 else 1 for i in statePlayers[4]]))
                    else: answer = ask_about_yahtzee(text_input.strip())

                    chat_history.append(("Bot", answer))
                    text_input = ""  # Reset input
        # go back button
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if pygame.Rect(MARGIN, MARGIN, 100, 40).collidepoint(mouse_pos):
                go_back = True

    pygame.draw.rect(screen, LIGHT_GREEN, (MARGIN, MARGIN, 100, 40))
    pygame.draw.rect(screen, BLACK, (MARGIN, MARGIN, 100, 40), 3)
    text = FONT.render("Go back", True, BLACK)
    text_rect = text.get_rect(center=(MARGIN + 50, MARGIN + 20))
    screen.blit(text, text_rect)

    # Function to split text into multiple lines
    def split_text_into_lines(text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.size(test_line)[0] > max_width:  # Check if line exceeds max width
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line
        if current_line:  # Append the last line
            lines.append(current_line)
        return lines

    # Draw chat history
    y_offset = HEIGHT - TEXT_BOX_HEIGHT - MARGIN * 2
    max_text_width = WIDTH - 2 * MARGIN
    for speaker, message in reversed(chat_history):
        chat_text = f"{speaker}: {message}"
        lines = split_text_into_lines(chat_text, FONT, max_text_width)
        for line in reversed(lines):  # Draw each line, bottom-up
            rendered_text = FONT.render(line, True, BLACK)
            text_height = rendered_text.get_height() + 5
            y_offset -= text_height
            if y_offset < 0:
                break  # Stop drawing if we run out of space
            screen.blit(rendered_text, (MARGIN, y_offset))

    # Draw text input box
    input_box_rect = pygame.Rect(
        MARGIN, HEIGHT - TEXT_BOX_HEIGHT - MARGIN, WIDTH - 120 - MARGIN * 2, TEXT_BOX_HEIGHT
    )
    pygame.draw.rect(screen, LIGHT_GRAY, input_box_rect)
    pygame.draw.rect(screen, DARK_GRAY, input_box_rect, 2)

    # Draw the current text input
    input_text_surface = FONT.render(text_input, True, BLACK)
    screen.blit(input_text_surface, (input_box_rect.x + 5, input_box_rect.y + 10))

    # Draw "Ask" button
    ask_button_rect = pygame.Rect(
        WIDTH - 100 - MARGIN, HEIGHT - TEXT_BOX_HEIGHT - MARGIN, 100, TEXT_BOX_HEIGHT
    )
    pygame.draw.rect(screen, GREEN, ask_button_rect)
    ask_text_surface = FONT.render("Ask", True, WHITE)
    ask_text_rect = ask_text_surface.get_rect(center=ask_button_rect.center)
    screen.blit(ask_text_surface, ask_text_rect)

    # Update the display
    pygame.display.flip()

def draw_screen(screen, statePlayers):
    global choose_button, row_chosen , can_choose_section, selected_dice, go_back
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # close the window
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Check for dice clicks
            toggle_dice_selection(mouse_pos)
            # Check for "Choose" button click
            if is_choose_button_clicked(mouse_pos):
                print("Choose button clicked!")
                choose_button = True
                selected_values = [i for i in range(NUM_DICE) if selected_dice[i]]
                print("Selected dice values:", selected_values)
                return selected_values
            if TABLE_X <= mouse_pos[0] <= TABLE_X + COLS * CELL_WIDTH and TABLE_Y <= mouse_pos[1] <= TABLE_Y + ROWS * CELL_HEIGHT:
                col = (mouse_pos[0] - TABLE_X) // CELL_WIDTH
                row = (mouse_pos[1] - TABLE_Y) // CELL_HEIGHT
                print("Clicked on cell:", row, col)
                row_chosen = True
                return row - 1
            if pygame.Rect(BUTTON_X, BUTTON_Y - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT).collidepoint(mouse_pos):
                print("Help button clicked!")
                go_back = False
                chat_history = []
                while go_back == False:
                    draw_help_screen(screen, statePlayers)

    screen.fill((0, 100, 0))

    # draw the table
    pygame.draw.rect(screen, (144, 238, 144), (TABLE_X, TABLE_Y, COLS * CELL_WIDTH, ROWS * CELL_HEIGHT))
    pygame.draw.rect(screen, (0, 0, 0), (TABLE_X, TABLE_Y, COLS * CELL_WIDTH, ROWS * CELL_HEIGHT), 3)

    # draw the grid
    for row in range(ROWS):
        for col in range(COLS):
            cell_x = TABLE_X + col * CELL_WIDTH
            cell_y = TABLE_Y + row * CELL_HEIGHT
            if row > 0 and col == 2 and row <= 13 and statePlayers[0] == 2 and can_choose_section[row - 1]:
                pygame.draw.rect(screen, (255, 255, 224), (cell_x, cell_y, CELL_WIDTH, CELL_HEIGHT), 1)
            else:
                pygame.draw.rect(screen, (0, 0, 0), (cell_x, cell_y, CELL_WIDTH, CELL_HEIGHT), 1)

            # fill the cell with text
            if row == 0:
                # header row
                text = FONT.render(header[col], True, TEXT_COLOR)
            elif col == 0:
                # combination names
                text = FONT.render(sectionsForPlayers[row - 1], True, TEXT_COLOR)
            else:
                # scores
                text = FONT.render('-' if statePlayers[col + 2][row - 1] == -1 else str(statePlayers[col + 2][row - 1]), True, TEXT_COLOR)

            text_rect = text.get_rect(center=(cell_x + CELL_WIDTH // 2, cell_y + CELL_HEIGHT // 2))
            screen.blit(text, text_rect)
    
    # draw the scores
    for row in range(1, ROWS):
        for col in range(1, COLS):
            cell_x = TABLE_X + col * CELL_WIDTH
            cell_y = TABLE_Y + row * CELL_HEIGHT
            text = FONT.render(str(), True, TEXT_COLOR)
            text_rect = text.get_rect(center=(cell_x + CELL_WIDTH // 2, cell_y + CELL_HEIGHT // 2))
            screen.blit(text, text_rect)

     # Draw the dice and choose button
    draw_dice()
    draw_choose_button()
    pygame.draw.rect(screen, LIGHT_GREEN, (BUTTON_X, BUTTON_Y - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, BLACK, (BUTTON_X, BUTTON_Y - BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_HEIGHT), 3)
    text = FONT.render("Help", True, BLACK)
    text_rect = text.get_rect(center=((BUTTON_X + BUTTON_WIDTH // 2,  BUTTON_Y - BUTTON_HEIGHT // 2 )))
    screen.blit(text, text_rect)

    text = FONT.render("Your turn" if statePlayers[0] == 2 else "AI turn", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH//4, 50))
    screen.blit(text, text_rect)

    pygame.display.flip()

def draw_feedback_screen(screen, statePlayers, decision_feedback):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if WIDTH // 4 - 100 <= mouse_pos[0] <= WIDTH // 4 + 100 and HEIGHT - 100 <= mouse_pos[1] <= HEIGHT - 60:
                    print("Go back button clicked!")
                    return

        screen.fill(WHITE)

        # change font size
        FONT = pygame.font.Font(None, 18)
        # Draw the feedback section on the right side
        feedback_box_x = 20 # Start drawing feedback section
        feedback_box_width = WIDTH - 40
        feedback_box_height = HEIGHT - 200
        feedback_box_y = 100

        # change font size back
        FONT = pygame.font.Font(None, 25)

        pygame.draw.rect(screen, WHITE, (feedback_box_x, feedback_box_y, feedback_box_width, feedback_box_height))
        pygame.draw.rect(screen, BLACK, (feedback_box_x, feedback_box_y, feedback_box_width, feedback_box_height), 3)

        # Print feedback inside the feedback box
        feedback_lines = decision_feedback.split('\n')  # Split the feedback into individual lines
        line_spacing = 20  # Spacing between lines
        feedback_y = feedback_box_y + 20  # Start 20px below the top of the box

        for line in feedback_lines:
            if feedback_y + line_spacing > feedback_box_y + feedback_box_height - 20:
                break  # Stop if we run out of space in the feedback box
            text = FONT.render(line, True, BLACK)
            text_rect = text.get_rect(topleft=(feedback_box_x + 10, feedback_y))
            screen.blit(text, text_rect)
            feedback_y += line_spacing

        # draw go back button
        pygame.draw.rect(screen, LIGHT_GREEN, (WIDTH // 4 - 100, HEIGHT - 100, 200, 40))
        pygame.draw.rect(screen, BLACK, (WIDTH // 4 - 100, HEIGHT - 100, 200, 40), 3)
        text = FONT.render("Go back", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 4, HEIGHT - 80))
        screen.blit(text, text_rect)

        pygame.display.flip()

def draw_end(screen, statePlayers, decision_feedback):
    global restart_game, FONT
    running = True  

    # Main loop for the end screen
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if WIDTH // 4 - 100 <= mouse_pos[0] <= WIDTH // 4 + 100 and HEIGHT - 100 <= mouse_pos[1] <= HEIGHT - 60:
                    print("Refresh button clicked!")
                    restart_game = True
                    main()
                    return  # Exit to restart the game
                if WIDTH // 4 - 100 <= mouse_pos[0] <= WIDTH // 4 + 100 and HEIGHT - 150 <= mouse_pos[1] <= HEIGHT - 110:
                    print("See feedback button clicked!")
                    # Show the feedback screen
                    draw_feedback_screen(screen, statePlayers, decision_feedback)


        screen.fill((0, 100, 0))

        for row in range(ROWS):
            for col in range(COLS):
                cell_x = WIDTH // 2 + col * CELL_WIDTH
                cell_y = 50 + row * CELL_HEIGHT
                pygame.draw.rect(screen, (144, 238, 144), (cell_x, cell_y, CELL_WIDTH, CELL_HEIGHT))
                pygame.draw.rect(screen, (0, 0, 0), (cell_x, cell_y, CELL_WIDTH, CELL_HEIGHT), 3)
                if row == 0:
                    # Header row
                    text = FONT.render(header[col], True, TEXT_COLOR)
                elif col == 0:
                    # Combination names
                    text = FONT.render(sectionsForPlayers[row - 1], True, TEXT_COLOR)
                else:
                    # Scores
                    text = FONT.render('-' if statePlayers[col + 2][row - 1] == -1 else str(statePlayers[col + 2][row - 1]), True, TEXT_COLOR)
                text_rect = text.get_rect(center=(cell_x + CELL_WIDTH // 2, cell_y + CELL_HEIGHT // 2))
                screen.blit(text, text_rect)

        text = FONT.render("Game Over!", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 4, 30))
        screen.blit(text, text_rect)

        text = FONT.render("You won!" if statePlayers[3][15] < statePlayers[4][15] else "You lost!", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 4, 60))
        screen.blit(text, text_rect)

        # draw see feedback button
        pygame.draw.rect(screen, LIGHT_GREEN, (WIDTH // 4 - 100, HEIGHT - 150, 200, 40))
        pygame.draw.rect(screen, BLACK, (WIDTH // 4 - 100, HEIGHT - 150, 200, 40), 3)
        text = FONT.render("See feedback", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 4, HEIGHT - 130))
        screen.blit(text, text_rect)

        # Draw refresh button
        pygame.draw.rect(screen, WHITE, (WIDTH // 4 - 100, HEIGHT - 100, 200, 40))
        pygame.draw.rect(screen, BLACK, (WIDTH // 4 - 100, HEIGHT - 100, 200, 40), 3)
        text = FONT.render("Restart", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 4, HEIGHT - 80))
        screen.blit(text, text_rect)

        pygame.display.flip()

def main(): 
    global AiMakesMove
    
    SetInitialState(statePlayers)
    print("Welcome to Medium Yahtzee! :)")
    print("Type 'help' during your turn to access the game assistant.")

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

    print("Start drawing the screen")
    draw_screen(screen, statePlayers)
    
    UpdatePlayerState(statePlayers)
  
def generate_decision_feedback(decision_vector):
    feedback = []

    for decision in decision_vector:
        turn_number, roll_number, chosen_dice, better_dice, dices = decision

        # Start feedback for the current decision
        if better_dice:
            feedback.append(
                f"On turn {turn_number}, roll {roll_number}, you chose {chosen_dice}, "
                f"but it would have been better to choose {better_dice}. {dices}"
            )
        else:
            feedback.append(
                f"On turn {turn_number}, roll {roll_number}, you chose {chosen_dice}, "
                f"which was a good decision. {dices}"
            )

    # Combine all feedback into a single text block
    return "\n".join(feedback)

#train the AI
for i in range(50):
    train_q_learning()

# Initial 
sectionsForPlayers = ["One", "Two", "Three", "Four", "Five", "Six", "3 of a kind", "4 of a kind", "Full House", "Small Straight", "Large Straight", "Yahtzee", "Chance", "Sum", "Bonus", "Final Score"]
statePlayers = list(range(5))

NUM_DICE = 5
selected_dice = [False] * NUM_DICE  # Track which dice are selected
# Dice positions
DICE_SIZE = 60
DICE_MARGIN = 10
DICE_X_START = 30
DICE_Y = 200
TEXT_BOX_HEIGHT = 50
MARGIN = 10

# Initialize pygame
pygame.init()

# Table dimensions and positioning
WIDTH, HEIGHT = 800, 600

# Screen dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yahtzee Game")

TABLE_X = WIDTH - 400  # X position of the table (right side)
TABLE_Y = 50           # Y position of the table
CELL_WIDTH = 130       # Width of each cell
CELL_HEIGHT = 30       # Height of each cell
ROWS = 17              # Total rows (1 header + 16 for combinations)
COLS = 3               # Total columns (Player Names + Scores)
TEXT_COLOR = (0, 0, 0)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (144, 238, 144)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# Choose button
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 40
BUTTON_X = 50
BUTTON_Y = HEIGHT - 100
choose_button = False
row_chosen = False
can_choose_section = [0 for _ in range(13)]
restart_game = False
go_back = False
chat_history = []
text_input = ""
dice_choices = []

decision_vector = []
round = 1

# Fonts
FONT = pygame.font.Font(None, 25)
header = ["Players", "Player 1", "Player 2"]


def decide_dice_to_keep(dice, scoring_state):
    # Prepare the current state
    current_state = (tuple(sorted(dice)), tuple(scoring_state))

    # Find the action with the highest Q-value
    best_action = max(
        range(13),
        key=lambda action: q_table.get((current_state, action), 0.0) if scoring_state[action] == 0 else -float('inf')
    )

    print(len(q_table))
    print("Best action:", best_action, )

    # Determine which dice to keep based on the best action
    indices_to_keep = []
    if 0 <= best_action <= 5:  # Ones to Sixes
        indices_to_keep = [i for i, d in enumerate(dice) if d == (best_action + 1)]
    elif best_action == 6:  # Three of a Kind
        indices_to_keep = [i for i, d in enumerate(dice) if dice.count(d) >= 3]
    elif best_action == 7:  # Four of a Kind
        indices_to_keep = [i for i, d in enumerate(dice) if dice.count(d) >= 4]
    elif best_action == 8:  # Full House
        indices_to_keep = [i for i, d in enumerate(dice) if dice.count(d) >= 2]
    elif best_action == 9:  # Small Straight
        # Prioritize sequences of 4 dice
        sequences = [[1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]]
        for seq in sequences:
            if all(x in dice for x in seq):
                indices_to_keep = [i for i, d in enumerate(dice) if d in seq]
                break
    elif best_action == 10:  # Large Straight
        indices_to_keep = list(range(len(dice)))  # Keep all dice
    elif best_action == 11:  # Yahtzee
        indices_to_keep = list(range(len(dice)))  # Keep all dice if they match
    elif best_action == 12:  # Chance
        indices_to_keep = [i for i, d in enumerate(dice) if d > 3]  # Keep high-value dice

    return indices_to_keep

main()