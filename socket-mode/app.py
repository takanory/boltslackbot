import os
import random
import re

from slack_bolt import Ack, App, BoltContext, Respond, Say
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk.web.client import WebClient

app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.message("hi")
def say_hello(message, say: Say):
    user = message['user']
    say(f"Hello, <@{user}>!")


def _choice(text: str):
    choiced = ""
    words = text.split()

    if len(words) == 1:
        choiced = random.choice(words[0])
    else:
        choiced = random.choice(words)
    return choiced


@app.message(re.compile(r"^\$choice\s(.*)"))
def choice(say: Say, context: BoltContext):
    say(_choice(context["matches"][0]))


@app.message(re.compile(r"^\$choice$"))
def choice_input(say: Say):
    blocks = [
        {
            "dispatch_action": True,
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "choice-action"
            },
            "label": {
                "type": "plain_text",
                "text": "文字列を入力してね",
                "emoji": True
            }
        }
    ]
    say(blocks=blocks)


@app.action("choice-action")
def choice_action(action: dict, ack: Ack, say: Say, respond: Respond):
    ack()
    value = action["value"]
    choiced = _choice(value)
    respond(f"`{value}` が入力されました")
    say(f"「{choiced}」が選ばれました")


@app.message(re.compile(r"^\$choice2$"))
def choice_modal(say: Say):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "ボタンを押すとモーダルが開くよ"
            },
            "accessory": {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "モーダルを開く",
                    "emoji": True
                },
                "value": "clicked",
                "action_id": "choice-modal"
            }
        }
    ]
    say(blocks=blocks)


@app.action("choice-modal")
def handle_choice_modal(ack: Ack, body: dict, context: BoltContext,
                        client: WebClient):
    ack()
    modal_view = {
        "type": "modal",
        "callback_id": "choice-modal-id",
        "title": {"type": "plain_text", "text": "choiceモーダル"},
        "submit": {"type": "plain_text", "text": "送信"},
        "close": {"type": "plain_text", "text": "キャンセル"},
        "blocks": [{
            "type": "input",
            "block_id": "input-block",
            "element": {
                "type": "plain_text_input",
                "action_id": "input-element",
            },
            "label": {
                "type": "plain_text",
                "text": "選択肢を書いてね",
                "emoji": True,
            },
        }],
        "private_metadata": context.channel_id,  # チャンネルIDを入れておく
    }

    client.views_open(
        trigger_id=body["trigger_id"],
        view=modal_view
    )


@app.view("choice-modal-id")
def handle_choice_modal_view(view: dict, ack: Ack, say: Say):
    inputs = view["state"]["values"]
    value = inputs["input-block"]["input-element"]["value"]
    choiced = _choice(value)
    channel_id = view["private_metadata"]
    ack()

    say(text=f"「{choiced}」が選ばれました", channel=channel_id)
    # respond(f"「{choiced}」が選ばれました")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
