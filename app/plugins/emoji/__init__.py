from app.launcher import Launcher
from app.launcher import Plugin as LauncherPlugin

from .commands import emoji


def init(launcher: Launcher):
    launcher.register_commands(emoji)
    print("Registering emoji plugin")


Plugin = LauncherPlugin(name="Emoji", init=init, is_enabled=False)
