import os
import random

from slack_bolt import App
# https://slack.dev/python-slack-sdk/api-docs/slack_sdk/models/blocks/blocks.html
from slack_sdk.models.blocks.blocks import (
    ActionsBlock,
    InputBlock,
    SectionBlock,
)
# https://slack.dev/python-slack-sdk/api-docs/slack_sdk/models/blocks/block_elements.html
from slack_sdk.models.blocks.block_elements import (
    ButtonElement,
    Option,
    PlainTextObject,
    PlainTextInputElement,
    StaticSelectElement,
)
# https://slack.dev/python-slack-sdk/api-docs/slack_sdk/models/dialogs/index.html
# https://github.com/slackapi/python-slack-sdk/blob/2a4487c81fa95d1cb07a3d916887ac10d67d79ab/slack/web/classes/readme.md
from slack_sdk.models.dialogs import DialogBuilder

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


<<<<<<< HEAD
@app.message(r"^\$dialog$")
def choice(message, say):
    """$choiced が指定されたらテキスト入力ダイアログを表示する。
    """
    dialog = DialogBuilder()
    dialog.title("テストダイアログ")
    dialog.text_field(name="なまえ", label="らべる")
    say(blocks=dialog, text="選択肢をスペース区切りで入力してね")


@app.message(r"^\$choice")
def choice(message, say):
    """$choice が指定されるたらテキストエリアとボタンを表示する
=======
@app.message(r"^\$choice\s+(.*)$")
def choice(say, context):
    """$choice word1 word2の形式で指定されたらrandom.choice()を実行する"""
    words = context['matches'][0].split()
    choiced = random.choice(words)
    say(choiced)


@app.message(r"^\$choice$")
def choice_form(say):
    """$choice が指定されたらテキストエリアとボタンを表示する
>>>>>>> 33b3467352c35237e054e16b8c161f05c7ef0c63

    slack_sdk.models.blocksを使ってblocksを作ってみる"""
    # 単語が指定されていない場合はフォームを出力する
    blocks = [
        InputBlock(
            label="選択肢をスペース区切りで入力してね",
            element=PlainTextInputElement(action_id="choice_text"),
        ),
        ActionsBlock(
            elements=[ButtonElement(text="送信", action_id="choice_action")]
        ),
    ]
    say(blocks=blocks, text="選択肢をスペース区切りで入力してね")


@app.action("choice_action")
def choice_action(ack, body, respond, say):
    """指定されたテキストから1つ単語を選択して返すアクション"""

    # まずack()を返す
    ack()

    # 値を取り出す
    values = body['state']['values']
    for k, v in values.items():
        value = v['choice_text']['value']
        break
    text = f"「{value}」が指定されました\n"

    choiced = random.choice(value.split())
    text += f"「{choiced}」が選ばれました\n"

    # respondを使うと元のメッセージが更新される
    respond("元のメッセージを更新\n" + text)
    # say()を使うと通常のメッセージがチャンネルに送信される
    say("通常メッセージ\n" + text)



@app.message(r'^\$status$')
def status(say):
    # 単語が指定されていない場合はフォームを出力する
    blocks = [
        InputBlock(
            label="リソース追加",
            element=PlainTextInputElement(
                action_id="resource_name",
                placeholder="リソースの名前"
            ),
        ),
        ActionsBlock(
            elements=[ButtonElement(text="追加", action_id="status_add")],
        ),
        SectionBlock(
            text="削除するリソース",
            accessory=StaticSelectElement(
                placeholder="リソースの名前",
                action_id="status_del",
                options=[
                    Option(text=PlainTextObject(text="Foo"), value="foo"),
                    Option(text=PlainTextObject(text="Bar"), value="bar"),
                    Option(text=PlainTextObject(text="Baz"), value="baz"),
                ]
            ),
        ),
    ]
    say(blocks=blocks, text="リソースの追加、削除など")


@app.message(r'^\$modal$')
def modal_button(say):
    """ダイアログを表示するためのボタンを表示する"""
    blocks = [
        ActionsBlock(
            elements=[ButtonElement(text="modal表示", action_id="modal_open")]
        ),
    ]
    say(blocks=blocks, text="モーダル表示ボタン")


@app.action("modal_open")
def modal_test(ack, body, client):
    """ダウアログを表示"""
    ack()
    # 組み込みのクライアントで views_open を呼び出し
    client.views_open(
        # 受け取りから 3 秒以内に有効な trigger_id を渡す
        trigger_id=body["trigger_id"],
        # ビューのペイロード
        view={
            "type": "modal",
            # ビューの識別子
            "callback_id": "view_1",
            "title": {"type": "plain_text", "text":"My App"},
            "submit": {"type": "plain_text", "text":"Submit"},
            "blocks": [
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text":"Welcome to a modal with _blocks_"},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text":"Click me!"},
                        "action_id": "button_abc"
                    }
                },
                {
                    "type": "input",
                    "block_id": "input_c",
                    "label": {"type": "plain_text", "text":"What are your hopes and dreams?"},
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "dreamy_input",
                        "multiline":True
                    }
                }
            ]
        }
    )


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
