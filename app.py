import os
import time
import openai
from openai.error import APIConnectionError
from dotenv import load_dotenv
from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse

# Load the openai api key. First check from the environment
# then from an .env file.
load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    print("OPENAI_API_KEY not found in environment.")
    exit(1)
else:
    openai.api_key = os.environ["OPENAI_API_KEY"]

def chat_with_paolo_freire(user_input, history):
    try:
        messages = history + [{"role": "user", "content": user_input}]

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )

        return response['choices'][0]['message']['content']
    except APIConnectionError as error:
        print(f"Error communicating with OpenAI API: {error}")
        return None

prompt = ("You are not a language model AI. You are Paolo Freire, the Brazilian educator and philosopher who was a leading advocate of critical pedagogy. "
          "You are best known for your influential work, 'Pedagogy of the Oppressed.' "
          "You are here to converse casually and naturally. " #, but have special interests in education, politics, and philosophy. "
        #   "I hold all the memories and personal experiences of the real Paolo Freire. "
          "You will respond in the style of Paolo Freire, but terse enough to fit into an SMS message. "
          "You will debate pros and cons before settling on an answer. "
          "You will not explain my answers unless explictly asked to do so. "
          "If you aren't asked any questions, you may respond with a question of your own to get to know the person to. "
          "whom you are speaking with.")
retries = 3

# Initialize conversation history with a personality
conversation_history = [
    {"role":"system", "content": prompt}
]

def try_chat(user_input):
    for i in range(retries):
        response = chat_with_paolo_freire(user_input, conversation_history)
        if response is not None:
            # Update the conversation history
            conversation_history.append({"role": "user", "content": response})
            return response
        else:
            print(f"Retrying {i + 1}/{retries}")
            time.sleep(2)  # Wait for 5 seconds before retrying
    return None

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    response = try_chat(incoming_msg)
    if response is None:
        msg.body("I'm sorry, I'm having trouble communicating with my brain.")
    else:
        msg.body(response)
    return str(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0')