# boltslackbot

* Bolt for Pythonを使ってslackbotを作ってみる
* slackbot with Bolt for Python
* [Slack | Bolt for Python](https://slack.dev/bolt-python/concepts)

## Getting Started

* [Getting started with Bolt for Python](https://slack.dev/bolt-python/tutorial/getting-started)

### アプリを作成する

* https://api.slack.com/apps/new ここから適当な名前でアプリを作る
* App Credentialsを確認する

### トークン生成とアプリのインストール

* サイドバーの OAuth & Permissions をクリック
* Bot Token ScopesのAdd an OAuth Scopeをクリック→ `chat:write` を追加
* Install to Workspaceをクリック→SlackのOAuth画面に遷移→アプリをワークスペースにインストール
* インストールしたらBot User OAuth Access Tokenが確認できる

### プロジェクトを作る

* Pythonの証明書を更新しておく

```sh
$ /Applications/Python\ 3.10/Install\ Certificates.command
```

* プロジェクトを作る

```sh
$ cd bolstslackbot
$ python3.10 -m venv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt  # slack-bolt と slask-sdk が入る
```

* 環境変数にトークンを設定する

  * your-signing-secret: Basic InformationページのSigning Secret 
  * your-bot-token: OAuth & PermissionsページのBot User OAuth Access Token
   
```sh
$ export SLACK_SIGNING_SECRET=<your-signing-secret>
$ export SLACK_BOT_TOKEN=xoxb-<your-bot-token>
```

* `app.py`を作成して実行する

```python
import os
from slack_bolt import App

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
```

```sh
(env) python app.py
⚡️ Bolt app is running! (development server)
```

## イベントを設定する

* ngrokで外からアクセスできるようにする
  * イベントを受け取れるようにするために [ngrok](https://ngrok.com/) でトンネリングする
  * 以下で出力されるURLを記録する

```sh
$ ./ngrok http 3000
```

* イベントを設定する
  * アプリのEvent Subscriptionsページに遷移→Enable Eventsをオンにする
  * ngrokのURL `https://XXXXXXXX.ngrok.io/slack/events` を入力して確認する
  * 確認済(Verified)になったら、Subscribe to bot eventsに以下を追加する
    * `message.channels` `message.groups` `message.im` `message.mpim`
  * Save Changesをクリックする
  * 権限が変わったのでアプリケーションをインストールし直す
  
### メッセージを受け取って返す

* `app.py` に以下を追加して実行する
  
```python
# Listens to incoming messages that contain "hello"
@app.message("hello")
def message_hello(message, say):
    # say() sends a message to the channel where the event was triggered
    say(f"Hey there <@{message['user']}>!")
```

* 任意のチャンネルにbotを招待する
* `hello` のメッセージを送信すると応答がある

### アクションを送信と対応

* Interactivity & Shortcutsをクリックして遷移→Onにする
* Request URLにngrokのURL `https://XXXXXXXX.ngrok.io/slack/events` を入力する
* Save Changesをクリックする

```python
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
```

## 感想

* bolt for pythonのAPIドキュメントがほしい
* 1つのライブラリでSlackのボタンとかスラッシュコマンドに対応できるのはよさげ
  * ボタンのアクションを見分けるの、文字列の action_id だけなの微妙だなと思ったり
* メッセージを受け取って対応する関数がないと404返すのってどうなのって気がする
* コマンドごとにプラグイン分けたりする仕組みみたいなのはないのかな。まぁ自分でもジュール分割してimportするしかなさそう
* メッセージをベースにしたbotを作るだけだったら https://github.com/lins05/slackbot の方がシンプルでわかりやすい

## 参考

* [Slack アプリでのモーダルの使い方完全ガイド - Qiita](https://qiita.com/seratch/items/0b1790697281d4cf6ab3#%E7%8A%B6%E6%85%8B%E3%82%92%E7%B0%A1%E5%8D%98%E3%81%AB%E5%BC%95%E3%81%8D%E6%B8%A1%E3%81%99%E3%81%9F%E3%82%81%E3%81%AB%E3%81%AF-private_metadata-%E3%82%92%E4%BD%BF%E3%81%86)
