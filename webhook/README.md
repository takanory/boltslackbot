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

* `*bold text*`
* `:emoji_name:`
* `<url|text>`
* 参考: [Formatting text for app surfaces](https://api.slack.com/reference/surfaces/formatting)

```python
response = webhook.send(text="Hello from\n*Pyton Slack SDK*! :tada:")
```

```python
response = webhook.send(text="Hello from *Pyton Slack SDK* (<https://slack.dev/python-slack-sdk/|URL>)!! :tada:")
```

## 参考

* [Sending messages using Incoming Webhooks | Slack](https://api.slack.com/messaging/webhooks)
* [Webhook Client](https://slack.dev/python-slack-sdk/webhook/index.html)
* [python-slack-sdk/slack_sdk/webhook](https://github.com/slackapi/python-slack-sdk/tree/main/slack_sdk/webhook)
* [Block Kit](https://api.slack.com/block-kit)