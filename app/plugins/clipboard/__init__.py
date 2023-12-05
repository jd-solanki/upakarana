import json
from dataclasses import asdict

from PyQt6.QtWidgets import QApplication

from app.launcher import Launcher
from app.launcher import Plugin as LauncherPlugin
from app.launcher import current_dir as launcher_dir

from .commands import clipboard
from .model import ClipboardItem


class ClipboardHandler:
    def __init__(self) -> None:
        self.init_clipboard()
        self.init_data_file()

        self.clipboard.dataChanged.connect(self.on_clipboard_change)  # type: ignore

    def init_data_file(self):
        self.clipboard_file_path = launcher_dir.parent / "clipboard.json"

        if self.clipboard.text():
            content = [ClipboardItem(self.clipboard.text(), None)]
            stringified_content = [asdict(item) for item in content]
            self.clipboard_file_path.write_text(
                json.dumps(stringified_content, indent=4)
            )

    def init_clipboard(self):
        clipboard = QApplication.clipboard()

        if clipboard:
            self.clipboard = clipboard
        else:
            raise Exception("Clipboard not found")

    def on_clipboard_change(self):
        print("Clipboard changed")
        clipboard_content = json.loads(self.clipboard_file_path.read_text())
        clipboard_content.insert(0, ClipboardItem(self.clipboard.text(), None))
        self.clipboard_file_path.write_text(json.dumps(clipboard_content, indent=4))


def init(launcher: Launcher):
    launcher.register_commands(clipboard)
    ClipboardHandler()
    print("Registering clipboard plugin")


Plugin = LauncherPlugin(name="Clipboard", init=init)
