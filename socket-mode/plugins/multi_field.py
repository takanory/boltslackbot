import json

from slack_bolt import Ack, App, Respond, Say

blocks_json = """
[
        {
            "type": "input",
            "element": {
                "type": "plain_text_input",
                "action_id": "name_action"
            },
            "label": {
                "type": "plain_text",
                "text": "名前",
                "emoji": true
            }
        },
        {
            "type": "input",
            "element": {
                "type": "static_select",
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select an item",
                    "emoji": true
                },
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "ほげ",
                            "emoji": true
                        },
                        "value": "value-0"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "ふが",
                            "emoji": true
                        },
                        "value": "value-1"
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "ぴよ",
                            "emoji": true
                        },
                        "value": "value-2"
                    }
                ],
                "action_id": "select-action"
            },
            "label": {
                "type": "plain_text",
                "text": "状態",
                "emoji": true
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
                        "emoji": true
                    },
                    "value": "click_me_123",
                    "action_id": "actionId-0"
                }
            ]
        }
    ]
"""


def enable_plugin(app: App) -> None:
    @app.message("hoge")
    def hoge(message: dict, say: Say) -> None:
        """Return morning greeting"""
        blocks = json.loads(blocks_json)
        say(blocks=blocks)

    @app.action("actionId-0")
    def hoge_action(action: dict, ack: Ack, body: dict, say: Say, respond: Respond):
        ack()
        respond("Respond()でメッセージを書き換えたよ")

        # 入力された値を取り出す
        for value in body["state"]["values"].values():
            match value:
                case {"name_action": {"value": name}}:
                    a_name = name
                case {"select-action": {"selected_option": {"text" :{"text": text}}}}:
                    a_text = text
        say(f"{a_name}、{a_text}を受け取りました")
