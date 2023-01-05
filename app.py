import os
import random

from flask import Flask, request, Response
from slack import WebClient
from slackeventsapi import SlackEventAdapter

import config

app = Flask(__name__)

SLACK_BOT_TOKEN = "xoxb-4575160099955-4577760292548-4GzQmTgUwNsDITmhZvgUolTn"
slack_event_adapter = SlackEventAdapter(config.SLACK_EVENTS_TOKEN, "/slack/events", app)
slack_web_client = WebClient(SLACK_BOT_TOKEN)


bot_id = slack_web_client.api_call("auth.test")['user_id']
MESSAGE_BLOCK = {
    "type": "section",
    "text" : {
        "type" : "mrkdwn",
        "text" : ""
    }
}
# slack_web_client.chat_postMessage(channel='#test',text='Hello')
@slack_event_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    text = event.get("text")
    channel_id = event.get("channel")
    user_id = event.get("user")
    if user_id != None and bot_id != user_id:
        if "flip a coin" in text.lower():
            rand_int = random.randint(0,1)
            if rand_int == 0:
                results = "Head"
            else:
                results = "Tail"
            message =  f"The result is {results}"
            MESSAGE_BLOCK["text"]["text"] = message
            message_to_send = {"channel": channel_id, "blocks": [MESSAGE_BLOCK]}
            return slack_web_client.chat_postMessage(**message_to_send)
        else:
            message = "unknown"
            MESSAGE_BLOCK["text"]["text"] = message
            message_to_send = {"channel": channel_id, "blocks": [MESSAGE_BLOCK]}
            return slack_web_client.chat_postMessage(**message_to_send)

@ app.route('/message-count', methods=['POST'])
def message_count():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')

    slack_web_client.chat_postMessage(
        channel=channel_id, text="I have got it")
    return Response(), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
