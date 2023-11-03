
from app.launcher import Launcher
from app.launcher import Plugin as LauncherPlugin

from .commands import about, reload


def init(launcher: Launcher):
    launcher.register_commands(reload)
    launcher.register_commands(about)
    print("Registering internal plugin")

Plugin = LauncherPlugin(name='Internal', init=init)