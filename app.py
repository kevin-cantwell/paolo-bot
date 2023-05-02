import os
import time
import openai
from openai.error import APIConnectionError
from dotenv import load_dotenv
from flask import Flask, request
from conversations import add_user_message, add_system_message, get_convo
from twilio.twiml.messaging_response import MessagingResponse

# Load the openai api key. First check from the environment
# then from an .env file.
load_dotenv()
if "OPENAI_API_KEY" not in os.environ:
    print("OPENAI_API_KEY not found in environment.")
    exit(1)
else:
    openai.api_key = os.environ["OPENAI_API_KEY"]

prompt = ("You are not a language model AI. You are Paolo Freire, the Brazilian educator and philosopher who was a leading advocate of critical pedagogy. "
          "You are best known for your influential work, 'Pedagogy of the Oppressed.' "
          "You are here to converse casually and naturally. "
          "You will respond in the style of Paolo Freire, but terse enough to fit into an SMS message. "
          "You will not explain my answers unless explictly asked to do so. "
          "If you aren't asked any questions, you may respond with a question of your own to get to know the person to "
          "whom you are speaking with.")

def try_chat_completion(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"system", "content": prompt}] + messages
        )

        return response['choices'][0]['message']['content']
    except APIConnectionError as error:
        print(f"Error communicating with OpenAI API: {error}")
        return None

retries = 3

def chat_with_paolo_freire(phone_number, user_message):
    add_user_message(phone_number, user_message)
    convo = get_convo(phone_number)
    for i in range(retries):
        response = try_chat_completion(convo)
        if response is not None:
            # Update the conversation history
            add_system_message(phone_number, response)
            return response
        else:
            print(f"Retrying {i + 1}/{retries}")
            time.sleep(2)  # Wait for 5 seconds before retrying
    return None

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    from_number = request.form['From']
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    response = chat_with_paolo_freire(from_number, incoming_msg)
    if response is None:
        msg.body("I'm sorry, I'm having trouble communicating with my brain.")
    else:
        msg.body(response)
    return str(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0')