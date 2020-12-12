import os
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
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


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
