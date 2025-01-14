# Hugging Face API token and endpoint
import requests


API_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"

# Set headers
headers = {"Authorization": f"Bearer {API_TOKEN}"}

# Ask your question
question = input("Ask a question: ")
payload = {"inputs": question}

# Make the API call
response = requests.post(API_URL, headers=headers, json=payload)

print("before answer")
# Parse and display the result
if response.status_code == 200:
    result = response.json()
    print(result[0]['generated_text'])

else:
    print(f"Error {response.status_code}: {response.text}")
print("after answer")