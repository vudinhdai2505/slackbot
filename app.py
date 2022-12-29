import os
import random

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

import config

app = Flask(__name__)


slack_event_adapter = SlackEventAdapter(config.SLACK_EVENTS_TOKEN, "/slack/events", app)
slack_web_client = WebClient(token=config.SLACK_BOT_TOKEN)


MESSAGE_BLOCK = {
    "type": "section",
    "text" : {
        "type" : "mrkdwn",
        "text" : ""
    }
}

@slack_event_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    text = event.get("text")
    if "flip a coin" in text.lower():
        channel_id = event.get("channel")
        rand_int = random.randint(0,1)
        if rand_int == 0:
            results = "Head"
        else:
            results = "Tail"
        message =  f"The result is {results}"
        MESSAGE_BLOCK["text"]["text"] = message
        message_to_send = {"channel": channel_id, "blocks": [MESSAGE_BLOCK]}
        return slack_web_client.chat_postMessage(**message_to_send)

@app.route('/')
def test():
    return "hello"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
