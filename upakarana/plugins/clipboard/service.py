import json

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtGui import QClipboard
from PyQt6.QtWidgets import QApplication

from upakarana.settings import PluginSettings

from .model import ClipboardItem

# ℹ️ We have to write PLUGIN_NAME here instead of entry file due to circular imports
PLUGIN_NAME = "clipboard"


class ClipboardWatcher(QObject):
    clipboard_changed = pyqtSignal(str)

    def __init__(self, clipboard: QClipboard, interval_in_ms: int = 500) -> None:
        super().__init__()
        self.clipboard = clipboard
        self.last_clipboard_content = None
        self.check_clipboard_timer = QTimer()
        self.check_clipboard_timer.timeout.connect(self.check_clipboard)  # type: ignore
        self.check_clipboard_timer.start(
            interval_in_ms
        )  # Check every `interval` milliseconds

    # ℹ️ This can't detect new clipboard content when copied without focus on the app on Ubuntu 22.10 (works on Mac & haven't tested on Windows)
    def check_clipboard(self):
        current_clipboard_content = self.clipboard.text()
        if current_clipboard_content != self.last_clipboard_content:
            self.last_clipboard_content = current_clipboard_content
            self.clipboard_changed.emit(current_clipboard_content)


class ClipboardHandler:
    def __init__(self) -> None:
        self.settings = PluginSettings(PLUGIN_NAME)

        self.init_clipboard()
        self.init_data_file()
        self.init_clipboard_watcher()

        self.clipboard.dataChanged.connect(self.on_clipboard_change)  # type: ignore

    def init_data_file(self):
        self.clipboard_file_path = self.settings.data_dir / "clipboard-data.json"

        if not self.clipboard_file_path.exists():
            self.clipboard_file_path.write_text("[]")

    def init_clipboard(self):
        clipboard = QApplication.clipboard()

        if clipboard:
            self.clipboard = clipboard
        else:
            raise Exception("Clipboard not found")

    def on_clipboard_change(self):
        content = self.clipboard.text()

        if not content:
            return

        self.add_item_to_clipboard(ClipboardItem(content=content, time=None))

    def init_clipboard_watcher(self):
        self.clipboard_watcher = ClipboardWatcher(self.clipboard)
        self.clipboard_watcher.clipboard_changed.connect(self.on_clipboard_change)  # type: ignore

    def add_item_to_clipboard(self, item: ClipboardItem):
        clipboard_content = json.loads(self.clipboard_file_path.read_text())

        if self.is_entry_exist(item, clipboard_content):
            clipboard_content.remove(item)

        clipboard_content.insert(0, item)

        # Write to file
        self.clipboard_file_path.write_text(json.dumps(clipboard_content, indent=4))

    def is_entry_exist(
        self, entry: ClipboardItem, clipboard_content: list[ClipboardItem]
    ) -> bool:
        for item in clipboard_content:
            if item.get("content") == entry.get("content"):
                return True

        return False

    def get_clipboard_content(self) -> list[ClipboardItem]:
        return json.loads(self.clipboard_file_path.read_text())
