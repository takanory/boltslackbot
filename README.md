# boltslackbot

* Bolt for Pythonを使ってslackbotを作ってみる
* slackbot with Bolt for Python
* [Slack | Bolt for Python](https://slack.dev/bolt-python/concepts)

## Getting Started

* [Getting started with Bolt for Python](https://slack.dev/bolt-python/tutorial/getting-started)
* Slackアプリを作成する
  * https://api.slack.com/apps/new ここから適当な名前でアプリを作る
  * App Credentialsを確認する
* トークンとアプリのインストール
  * サイドバーの OAuth & Permissions をクリック
  * Bot Token ScopesのAdd an OAuth Scopeをクリック→ `chat:write` を追加
  * Install to Workspaceをクリック→SlackのOAuth画面に繊維→アプリをワークスペースにインストール
  * インストールしたらBot User OAuth Access Tokenが確認できる
* Pythonの証明書を更新しておく

```sh
$ /Applications/Python\ 3.9/Install\ Certificates.command
```

* プロジェクトを作る

```sh
$ cd bolstslackbot
$ python3.9 -m venv env
$ source env/bin/activate
(env) $ pip install slack_bolt
```

* 環境変数に設定する

  * your-signing-secret: Basic InformationページのSigning Secret 
  * your-bot-token: OAuth & PermissionsページのBot User OAuth Access Token
   
```sh
$ export SLACK_SIGNING_SECRET=<your-signing-secret>
$ export SLACK_BOT_TOKEN=xoxb-<your-bot-token>
```

* app.pyを作成して実行する

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
