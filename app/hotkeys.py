# ❗This is in experimental stage due to the fact that it's hard to implement hotkeys in a cross-platform way globally (outside of the app window)
# ℹ️ If you have any idea how to implement this, please feel free to make PR or open an issue to discuss it.

from pynput import keyboard
from pynput.keyboard import Key, KeyCode
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QMainWindow


class HotKeys(QObject):
    show_signal = pyqtSignal()

    def __init__(self, main_window: QMainWindow):
        super().__init__()

        self.main_window = main_window

        self.hotkey = keyboard.HotKey(
            keyboard.HotKey.parse("<alt>+<space>"), self.show_window
        )
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

        # Execute the function in the main thread when the show signal is emitted
        self.show_signal.connect(self.main_window.show)  # type: ignore
        self.show_signal.connect(self.main_window.activateWindow)  # type: ignore

    def show_window(self):
        # We need to emit the signal instead of calling the function directly due to GUI threading
        self.show_signal.emit()

    def on_press(self, key: Key | KeyCode | None):
        if key:
            self.hotkey.press(key)

    def on_release(self, key: Key | KeyCode | None):
        if key:
            self.hotkey.release(key)
