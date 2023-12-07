from upakarana import App
from upakarana.launcher import Launcher
from upakarana.launcher import Plugin as LauncherPlugin

from .commands import clipboard
from .service import ClipboardHandler


def init(launcher: Launcher):
    launcher.register_commands(clipboard)
    ClipboardHandler()
    app = App()
    app._clipboard_handler = ClipboardHandler()  # type: ignore
    print("Registering clipboard plugin")


Plugin = LauncherPlugin(name="Clipboard", init=init)
