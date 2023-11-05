from app.launcher import Launcher
from app.launcher import Plugin as LauncherPlugin

from .commands import clipboard


def init(launcher: Launcher):
    launcher.register_commands(clipboard)
    print("Registering clipboard plugin")


Plugin = LauncherPlugin(name="Clipboard", init=init)
