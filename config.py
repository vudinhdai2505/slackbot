import os
from dotenv import load_dotenv
load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_EVENTS_TOKEN = os.getenv("SLACK_EVENTS_TOKEN")
