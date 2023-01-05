import random

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

import config

app = Flask(__name__)

SLACK_BOT_TOKEN = "xoxb-4575160099955-4577760292548-MOl3pl7384bz8xOmPNVt8DiU"
slack_event_adapter = SlackEventAdapter(config.SLACK_EVENTS_TOKEN, "/slack/events", app)
slack_web_client = WebClient(SLACK_BOT_TOKEN)


