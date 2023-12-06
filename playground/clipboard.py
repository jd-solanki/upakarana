import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow

@dataclass
class ClipboardItem:
    content: str
    time: str | None

class ClipboardWatcher(QObject):
    clipboard_changed = pyqtSignal(str)

    def __init__(self, clipboard, interval=1000) -> None:
        super().__init__()
        self.clipboard = clipboard
        self.last_clipboard_content = None
        self.check_clipboard_timer = QTimer()
        self.check_clipboard_timer.timeout.connect(self.check_clipboard)
        self.check_clipboard_timer.start(interval)  # Check every `interval` milliseconds

    def check_clipboard(self):
        print(f"cjecki...")
        current_clipboard_content = self.clipboard.text()
        if current_clipboard_content != self.last_clipboard_content:
            self.last_clipboard_content = current_clipboard_content
            self.clipboard_changed.emit(current_clipboard_content)

class ClipboardHandler:
    def __init__(self, clipboard_file_path: Path) -> None:
        self.clipboard_file_path = clipboard_file_path

    def handle_clipboard_change(self, content):
        print("Clipboard changed", content)
        # Process clipboard change here, e.g., save to file
        clipboard_item = ClipboardItem(content, None)
        self.save_clipboard_content(clipboard_item)

    def save_clipboard_content(self, item: ClipboardItem):
        stringified_content = asdict(item)
        with self.clipboard_file_path.open("a") as file:
            json.dump(stringified_content, file, indent=4)
            file.write("\n")

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My App")
        label = QLabel(text="This is a PyQt6 window!")
        
        self.clipboard_file_path = Path("clipboard-content.json")
        self.clipboard_handler = ClipboardHandler(self.clipboard_file_path)
        self.clipboard_watcher = ClipboardWatcher(QApplication.clipboard())
        self.clipboard_watcher.clipboard_changed.connect(self.clipboard_handler.handle_clipboard_change)

        self.setCentralWidget(label)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()