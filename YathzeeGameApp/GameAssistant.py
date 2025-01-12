import os
import openai
from typing import Dict, List, Optional

class YahtzeeGameAssistant:
    def __init__(self, api_key: str):
        """Initialize the game assistant with OpenAI API credentials."""
        openai.api_key = api_key
        self.conversation_history: List[Dict] = []
        self.context = """
        You are a Yahtzee game assistant. Help players understand the rules, provide strategic advice,
        and analyze game situations. Consider the following aspects when giving advice:
        - Optimal dice selection strategies
        - Score sheet management
        - Probability-based decision making
        - Common scenarios and best practices
        """

    def format_game_state(self, state_players: list) -> str:
        """Format the current game state for the AI assistant."""
        ai_score = [i if i != -1 else '-' for i in state_players[3][0:13]]
        player_score = [i if i != -1 else '-' for i in state_players[4][0:13]]
        
        return f"""
        Current Game State:
        AI Player: {ai_score} (Total: {state_players[3][15]})
        Human Player: {player_score} (Total: {state_players[4][15]})
        Current Dice: {state_players[2]}
        """

    async def get_game_advice(self, 
                            question: str, 
                            state_players: Optional[list] = None,
                            temperature: float = 0.7) -> str:
        """
        Get game advice from the AI assistant based on the question and current game state.
        """
        prompt = f"{self.context}\n"
        
        if state_players:
            prompt += f"\nCurrent game state:\n{self.format_game_state(state_players)}\n"
        
        prompt += f"\nPlayer question: {question}"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt},
                    *self.conversation_history,
                    {"role": "user", "content": question}
                ],
                temperature=temperature,
                max_tokens=300
            )
            
            answer = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.extend([
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer}
            ])
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
                
            return answer

        except Exception as e:
            return f"Sorry, I couldn't process your question. Error: {str(e)}"

def create_game_menu():
    """Create an interactive menu for game assistance."""
    print("\n=== Yahtzee Game Assistant ===")
    print("1. Ask about rules")
    print("2. Get strategic advice")
    print("3. Analyze current situation")
    print("4. Practice scenarios")
    print("5. Return to game")
    print("===========================")

async def handle_assistance(game_assistant: YahtzeeGameAssistant, state_players: list):
    """Handle player requests for game assistance."""
    while True:
        create_game_menu()
        choice = input("\nEnter your choice (1-5): ")

        if choice == "5":
            return

        questions = {
            "1": "Can you explain the basic rules of Yahtzee?",
            "2": "What are some general strategies for playing Yahtzee well?",
            "3": "Given my current game state, what would you recommend?",
            "4": "Can you provide a practice scenario to help me improve?"
        }

        if choice in questions:
            if choice == "3":
                # For situation analysis, include the current game state
                response = await game_assistant.get_game_advice(questions[choice], state_players)
            else:
                response = await game_assistant.get_game_advice(questions[choice])
            
            print("\nAssistant's Response:")
            print(response)
            
            follow_up = input("\nWould you like to ask a follow-up question? (y/n): ")
            if follow_up.lower() == 'y':
                question = input("\nEnter your question: ")
                response = await game_assistant.get_game_advice(question, state_players)
                print("\nAssistant's Response:")
                print(response)
        
        input("\nPress Enter to continue...")

def initialize_assistant() -> YahtzeeGameAssistant:
    """Initialize the game assistant with API credentials."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("API key not found. Please set the OPENAI_API_KEY environment variable.") 
    return YahtzeeGameAssistant(api_key)
