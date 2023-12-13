from PyQt6.QtCore import QThreadPool
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedLayout,
    QStatusBar,
    QWidget,
)

from upakarana.events import Events
from upakarana.settings import Settings


class App:
    is_hotkeys_disabled = True
    _instance = None
    _main_window: QMainWindow | None = None
    stacked_layout: QStackedLayout = QStackedLayout()
    events: Events = Events()
    settings = Settings()
    threadpool = QThreadPool()
    _statusBar: QStatusBar | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls)
        return cls._instance

    @property
    def main_window(self) -> QMainWindow:
        if self._main_window is None:
            raise Exception("Main window not initialized")

        return self._main_window

    @main_window.setter
    def main_window(self, main_window: QMainWindow):
        self._main_window = main_window

    def set_font(self, widget: QWidget, font_size: int | None = None):
        font = QApplication.font()
        if font_size:
            font.setPointSize(font_size)
        widget.setFont(font)

    @property
    def status_bar(self) -> QStatusBar:
        if self._statusBar is None:
            raise Exception("Status bar not initialized")

        return self._statusBar

    @status_bar.setter
    def status_bar(self, status_bar: QStatusBar):
        self._statusBar = status_bar
