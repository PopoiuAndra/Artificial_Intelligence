import openai

# Set up the environment to use the Ollama server
openai.api_base = "http://localhost:11434/v1"
openai.api_key = "ollama"  # Placeholder; Ollama typically doesn't require a key.

def ask_about_yahtzee(question):
    """
    Function to ask a question to the Ollama model about Yahtzee.
    Args:
        question (str): The user's question about Yahtzee.
    Returns:
        str: The model's response or a message if an error occurs.
    """
    try:
        # Send the question to the Ollama server
        response = openai.ChatCompletion.create(
            model="llama3.2",  # Replace with the correct model name if different
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant for the game Yahtzee. "
                        "Only answer questions about the game. "
                        "Do not provide any other information. "
                        "Try to be as helpful as possible. "
                        "You will be asked questions by a user. "
                        "Answer them to the best of your ability. "
                        "Answer in short sentences."
                    ),
                },
                {"role": "user", "content": question},
            ],
        )
        # Return the response content
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

# Main script
if __name__ == "__main__":
    print("Ask questions about Yahtzee and its rules! Type 'exit' to quit.")
    while True:
        user_question = input("\nYour question: ")
        if user_question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        # Query the model and print the response
        answer = ask_about_yahtzee(user_question)
        print(f"\nOllama's answer: {answer}")
