from upakarana.launcher import Launcher
from upakarana.launcher import Plugin as LauncherPlugin

from .commands import repositories


def init(launcher: Launcher):
    launcher.register_commands(repositories)
    print("Registering GitHub plugin")


Plugin = LauncherPlugin(name="GitHub", init=init)
