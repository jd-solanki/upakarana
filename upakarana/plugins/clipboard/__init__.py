from upakarana import App
from upakarana.launcher import Launcher
from upakarana.launcher import Plugin as LauncherPlugin

from .commands import clipboard

# ℹ️ We have to write `PLUGIN_NAME` in `service.py` instead of here due to circular imports
from .service import PLUGIN_NAME, ClipboardHandler


def init(launcher: Launcher):
    launcher.register_commands(clipboard)
    ClipboardHandler()
    app = App()
    app._clipboard_handler = ClipboardHandler()  # type: ignore
    print("Registering clipboard plugin")


Plugin = LauncherPlugin(name=PLUGIN_NAME, init=init)
