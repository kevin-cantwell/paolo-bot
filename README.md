# Paolo Bot

Paolo Bot is an SMS chatbot that impersonates the Brazilian educator and philosopher and author of the book "The Pedagogy of the Oppressed". I built it to troll my friend who likes to argue a lot. When I get annoyed I just send him the number to Paolo Bot and he argues with it instead of me.

## How it works

Paolo Bot is a Twilio webhook for SMS interaction. It uses the Twilio API to send and receive SMS messages. It uses the `twilio` module to parse incoming SMS messages and generate responses. It uses the OpenAI api to generate chat responses. Conversations with unique phone numbers are persisted in Redis. Over time, older messages in a conversation will be "forgotten" in order to keep service costs to a minimum.

## How to use it

Send an SMS message to the Twilio number you have assigned to this bot. Paolo Bot will respond with a message. You can continue the conversation as long as you like. If the total tokens in your conversation exceed `MAX_TOKENS`, Paolo Bot will begin to forget earlier portions of the conversation.

## How to run it as a command-line chatbot

You can run the bot locally with `python bot.py`. In this form, it acts as a command-line chatbot and only interacts with OpenAI--no need for a Twilio account. You will need to set the following environment variables: `OPENAI_API_KEY` and `REDISCLOUD_URL`.

## How to configure it to run as a SMS web hook

You can deploy it to a public web hosting provider that Twilio can communicate with. This repo is pre-configured to run on Heroku.

You must create a `.env` file in the root directory of this project. It should contain the following environment variables:

```
OPENAI_API_KEY=replaceme
TWILIO_ACCOUNT_ID=replaceme
TWILIO_AUTH_TOKEN=replaceme
REDISCLOUD_URL=replaceme
MAX_TOKENS=500
```

You can get your Twilio account ID and auth token from your Twilio account dashboard. You can get your OpenAI API key from your OpenAI account dashboard. You can get your Redis URL from your Redis hosting provider. I use Redis Cloud.

You must configure your Twilio account to use the webhook provided by this app. You can do this from your Twilio account dashboard. You must also configure your Twilio account to use a phone number. You can do this from your Twilio account dashboard. You can use a free phone number for this.

Your webhook must look like `https://yourappname.herokuapp.com/bot`. You can use the cheapest tier of Heroku to host this app.

