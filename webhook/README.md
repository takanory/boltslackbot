# Webhook

## Webhookを作る

* Slack appを作る
  * https://api.slack.com/apps?new_app=1
  * From scratch
  * App Nameを入力してworkspaceを選択
* Incoming Webhooksを有効にする
  * 「App features and functionality」で「Incoming Webhooks」をクリック
  * 右上のOff→On
* Webhookを追加
  * 「Add New Webhook to Workspace」をクリック
  * チャンネルを選択して「Allow」
  * SlackチャンネルにもWebhookが追加されたことがわかる
* Webhook URLが取得できる
  * `https://hooks.slack.com/services/T000...

## メッセージを送信

* curlコマンドでメッセージを送信

```bash
$ curl -X POST -H 'Content-type: application/json' \
  --data '{"text":"Hello Slack!"}' \
  https://hooks.slack.com/services/T000...
```

* Pythonのurllib.requestでメッセージを送信

```python
import json
from urllib import request

url = "https://hooks.slack.com/services/T000..."
message = {"text": "Hello from Python!"}
data = json.dumps(data).encode()
request.urlopen(url, data=data)
```

* [Requests](https://docs.python-requests.org/)でメッセージを送信

```bash
$ python3.10 -m venv env
$ . env/bin/activate
(env)$ pip install requests
```

```python
import requests

url = "https://hooks.slack.com/services/T000..."
message = {"text": "Hello from Requests!"}
requests.post(url, json=message)
```

* [Python Slack SDK](https://slack.dev/python-slack-sdk/) でメッセージを送信

```bash
$ python3.10 -m venv env
$ . env/bin/activate
(env)$ pip install slack-sdk
```

```python
from slack_sdk.webhook import WebhookClient

url = "https://hooks.slack.com/services/T000..."
webhook = WebhookClient(url)
response = webhook.send(text="Hello from Pyton Slack SDK!")
```

## メッセージをリッチにする

### テキストのフォーマット

* `\n`、`*bold text*`、`:emoji_name:`、`<url|text>`
* 参考: [Formatting text for app surfaces](https://api.slack.com/reference/surfaces/formatting)

```python
response = webhook.send(text="Hello from\n*Pyton Slack SDK*! :tada:")
```

```python
response = webhook.send(text="Hello from *Pyton Slack SDK* (<https://slack.dev/python-slack-sdk/|URL>)!! :tada:")
```

### Message Attachments

* 現在はLayout Blocks(後述)が推奨されている
* 参考: [Reference: Secondary message attachments | Slack](https://api.slack.com/reference/messaging/attachments)

```python

fields = [
    {"title": "Love", "value": ":beer:, Ferrets, LEGO", "short": True},
    {"title": "From", "value": "Japan :jp:", "short": True},
]
attachments =  [{
    "pretext": "Nice to meet you!!",
    "author_name": "Takanori Suzuki",
    "author_link": "https://twitter.com/takanory/",
    "text": "*THANK YOU* for coming to my talk !:tada: Please give me *feedback* about this talk :bow:",
    "fields": fields,
}]

response = webhook.send(attachments=attachments, unfurl_links=["https://twitter.com/takanory"])
```

### Layout Blocks

* 参考
  * [Block Kit](https://api.slack.com/block-kit)
  * [Reference: Layout blocks](https://api.slack.com/reference/block-kit/blocks)

## 参考

* [Sending messages using Incoming Webhooks | Slack](https://api.slack.com/messaging/webhooks)
* [Webhook Client](https://slack.dev/python-slack-sdk/webhook/index.html)
* [python-slack-sdk/slack_sdk/webhook](https://github.com/slackapi/python-slack-sdk/tree/main/slack_sdk/webhook)
* [Block Kit](https://api.slack.com/block-kit)
