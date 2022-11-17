from slack_bolt import App, Say


def enable_plugin(app: App) -> None:
    @app.message("おはよう")
    def morning(message: dict, say: Say) -> None:
        """Return morning greeting"""
        say("おはよう")
