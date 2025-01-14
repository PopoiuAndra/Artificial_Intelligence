import random
import requests
from EasyDifficultAI import IsFinalState, ScoreCalculation

# Initial Configuration
sectionsForPlayers = ["One", "Two", "Three", "Four", "Five", "Six", "3 of a kind", "4 of a kind", "Full House", "Small Straight", "Large Straight", "Yahtzee", "Chance", "First 6 sections score", "Bonus", "Final Score"]

# Hugging Face API Configuration
HUGGING_FACE_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
HUGGING_FACE_API_KEY = "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" 

def query_assistant(prompt):
    """Query the Hugging Face API for an assistant response."""
    headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
    payload = {"inputs": prompt}

    try:
        response = requests.post(HUGGING_FACE_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        # Hugging Face API returns a list of dictionaries
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            generated_text = result[0].get("generated_text", "Sorry, I couldn't understand that.")
        else:
            generated_text = "Unexpected response format from the API."
        return generated_text
    except requests.exceptions.RequestException as e:
        return f"Error contacting the assistant: {e}"


def evaluate_state(state_players):
    """
    Evaluates the current game state from AI's perspective.
    Returns a score representing how good the state is for the AI.
    """
    ai_score = state_players[3][15]  # AI's current total score
    human_score = state_players[4][15]  # Human's current total score
    return ai_score - human_score

def get_possible_dice_combinations(current_dice):
    """
    Generates possible dice combinations after rerolling non-kept dice.
    Returns a list of possible dice combinations.
    """
    combinations = []
    kept_positions = [i for i, val in enumerate(current_dice) if val != 0]
    
    # For simplicity, we'll generate a limited number of combinations
    for _ in range(10):  # Limiting to 10 possible combinations for performance
        new_dice = current_dice.copy()
        for i in range(5):
            if i not in kept_positions:
                new_dice[i] = random.randint(1, 6)
        combinations.append(new_dice)
    return combinations

def get_available_sections(state_players, player_index, score):
    """
    Returns list of available sections that can be chosen.
    """
    available = []
    for i in range(13):
        if state_players[player_index][i] == -1 and score[i] != 0:
            available.append(i)
    if not available:
        return [i for i in range(13) if state_players[player_index][i] == -1]
    return available

def minimax(state_players, depth, is_maximizing, alpha, beta):
    """
    Minimax algorithm with alpha-beta pruning for decision making.
    Returns the best score and the corresponding move (dice to keep and section to choose).
    """
    if depth == 0 or IsFinalState(state_players):
        return evaluate_state(state_players), None, None

    if is_maximizing:  # AI's turn
        max_eval = float('-inf')
        best_dice = None
        best_section = None
        
        # Generate possible dice combinations
        possible_dice = get_possible_dice_combinations(state_players[2])
        
        for dice in possible_dice:
            score = ScoreCalculation(dice)
            available_sections = get_available_sections(state_players, 3, score)
            
            for section in available_sections:
                # Create a copy of the state and simulate the move
                new_state = [state_players[i].copy() if isinstance(state_players[i], list) 
                           else state_players[i] for i in range(len(state_players))]
                new_state[3][section] = score[section]
                
                # Update scores
                new_state[3][13] = sum([i for i in new_state[3][0:6] if i != -1])
                new_state[3][14] = 35 if sum(new_state[3][0:6]) >= 63 else 0
                new_state[3][15] = sum([i for i in new_state[3][0:13] if i != -1]) + new_state[3][14]
                
                eval, _, _ = minimax(new_state, depth - 1, False, alpha, beta)
                
                if eval > max_eval:
                    max_eval = eval
                    best_dice = dice
                    best_section = section
                
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
                    
        return max_eval, best_dice, best_section
    
    else:  # Human's turn (minimizing)
        min_eval = float('inf')
        best_dice = None
        best_section = None
        
        # Simulate simplified human moves
        possible_dice = get_possible_dice_combinations(state_players[2])
        
        for dice in possible_dice:
            score = ScoreCalculation(dice)
            available_sections = get_available_sections(state_players, 4, score)
            
            for section in available_sections:
                new_state = [state_players[i].copy() if isinstance(state_players[i], list) 
                           else state_players[i] for i in range(len(state_players))]
                new_state[4][section] = score[section]
                
                # Update scores
                new_state[4][13] = sum([i for i in new_state[4][0:6] if i != -1])
                new_state[4][14] = 35 if sum(new_state[4][0:6]) >= 63 else 0
                new_state[4][15] = sum([i for i in new_state[4][0:13] if i != -1]) + new_state[4][14]
                
                eval, _, _ = minimax(new_state, depth - 1, True, alpha, beta)
                
                if eval < min_eval:
                    min_eval = eval
                    best_dice = dice
                    best_section = section
                    
                beta = min(beta, eval)
                if beta <= alpha:
                    break
                    
        return min_eval, best_dice, best_section

def AiMakesMoveMedium(state_players):
    """
    Updated AI move function using minimax strategy.
    """
    # Initial dice roll
    if state_players[2].count(0) == 5:
        state_players[2] = [random.randint(1, 6) for _ in range(5)]
    
    print("AI Player initial dice:", state_players[2])
    
    # Use minimax to decide the best move
    _, best_dice, best_section = minimax(state_players, depth=3, is_maximizing=True, 
                                       alpha=float('-inf'), beta=float('inf'))
    
    if best_dice is not None:
        state_players[2] = best_dice
    
    if best_section is not None:
        score = ScoreCalculation(state_players[2])
        state_players[3][best_section] = score[best_section]
        
        # Update scores
        state_players[3][13] = sum([i for i in state_players[3][0:6] if i != -1])
        state_players[3][14] = 35 if sum(state_players[3][0:6]) >= 63 else 0
        state_players[3][15] = sum([i for i in state_players[3][0:13] if i != -1]) + state_players[3][14]
        
        print("AI Player chose the section", sectionsForPlayers[best_section], 
              "with score:", score[best_section])
    
    # Reset dice for next turn
    state_players[1] = 4
    state_players[2] = [0, 0, 0, 0, 0]
    
    return state_players


while (True):
    prompt = input("Ask a question: ")
    response = query_assistant(prompt)
    print(f"Response: {response}\n")