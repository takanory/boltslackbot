import logging
import os

from slack_bolt import App, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler

from plugins import enable_plugins

logging.basicConfig(level=logging.DEBUG)

app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.message("hi")
def say_hello(message, say: Say):
    user = message['user']
    say(f"Hello, <@{user}>!")


enable_plugins(app)


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
