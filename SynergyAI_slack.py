import os
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"
app = Flask(__name__)
# Initializes your app with your bot token and signing secret
slack_app = App(
    token="xoxb-5568538082343-5601729811140-5okmA1MJzTyce7VC1bzOdgPY",
    signing_secret="2f94b59c1ba1b8d0ce18b9d3f229eea7",
    raise_error_for_unhandled_request=True
)

slack_handler = SlackRequestHandler(slack_app)

# This will match any message that contains "Hello"
@slack_app.message("")
def answer(message, say):
    user = message['user']
    text = message['text']
    print(message['channel'])
    # say(f"Hello, glad to see you <@{user}>!")
    say(channel=message['channel'],text=get_from_chatgpt(text))

@app.route("/slack/events", methods=["POST"])
def slack_events():
    return slack_handler.handle(request)

def get_from_chatgpt(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: {prompt}\nAI:",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    response = response['choices'][0]['text']
    return response

# Start your app
if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)))
    
