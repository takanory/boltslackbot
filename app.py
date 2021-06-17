import os
import random
import time

from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"こんにちは <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"こんにちは <@{message['user']}>!"
    )


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


@app.message(r"^\$choice")
def choice(message, say):
    """$choice が指定されるたらテキストエリアとボタンを表示する"""
    blocks = [
        {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "choice_text",
            },
            "label": {
                "type": "plain_text",
                "text": "選択肢をスペース区切りで入力してね",
                "emoji": True,
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "送信",
                        "emoji": True,
                    },
                    "value": "send",
                    "action_id": "choice_action"
                }
            ]
        }
    ]
    say(blocks=blocks, text="選択肢をスペース区切りで入力してね")


@app.action("choice_action")
def choice_action(ack, body, respond, say):
    """指定されたテキストから1つ単語を選択して返すアクション"""
    ack()
    values = body['state']['values']
    for k, v in values.items():
        value = v['choice_text']['value']
        break
    text = f"「{value}」が指定されました\n"
    for i in range(5):  # 5秒sleepして5回送信する
        choiced = random.choice(value.split())
        text += f"{i+1}回目は「{choiced}」が選ばれました\n"
        # respondを使うと元のメッセージが更新される
        respond(text)
        # 普通のsayを使ったメッセージ送信もできる
        say(f"{i+1}回目は「{choiced}」が選ばれました")
        time.sleep(5)


@app.message("こんにちは")
def message_konnnichiwa(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"こんにちは <@{message['user']}>!今日はなにを飲みますか?"}
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": ":beer:",
                            "emoji": True,
                        },
                        "value": "click_me_123",
                        "action_id": "button_beer",
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": ":coffee:",
                            "emoji": True,
                        },
                        "value": "click_me_123",
                        "action_id": "button_coffee",
                    }
                ]
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )


@app.action("button_beer")
def action_button_beer(body, ack, say):
    ack()
    say(f"<@{body['user']['id']}> やっぱりビールだよね!!!")


@app.action("button_coffee")
def action_button_coffee(body, ack, say):
    ack()
    say(f"<@{body['user']['id']}> コーヒーとかないわー...")


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
