from slack_bolt import App

from . import choice, multi_field


def enable_plugins(app: App) -> None:
    choice.enable_plugin(app)
    multi_field.enable_plugin(app)
