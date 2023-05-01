import os
import openai
from dotenv import load_dotenv

# Load the openai api key. First check from the environment
# then from an .env file.
if "OPENAI_API_KEY" in os.environ:
    openai.api_key = os.environ["OPENAI_API_KEY"]
else:
    load_dotenv()

def chat_with_paolo_freire(user_input, conversation_history):
    paolo_freire_context = "Paolo Freire was a Brazilian educator and philosopher who was a leading advocate of critical pedagogy. He is best known for his influential work, 'Pedagogy of the Oppressed,' which is considered one of the foundational texts of the critical pedagogy movement."

    messages=[
        {"role": "system", "content": paolo_freire_context}
    ]
    messages = messages + conversation_history

    prompt = f"{paolo_freire_context}\n\n{conversation_history}User: {user_input}\nPaolo Freire:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response['choices'][0]['message']['content']

# Initialize an empty conversation history
conversation_history = []

while True:
    user_input = input("User: ")
    if user_input.lower() == "quit":
        break

    response = chat_with_paolo_freire(user_input, conversation_history)
    print(f"Paolo Freire: {response}")

    # Update the conversation history
    conversation_history += {"role": "user", "content": response}


