import sys
from typing import cast, override

from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QGuiApplication, QKeyEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedLayout, QWidget

from upakarana import App
from upakarana.hotkeys import HotKeys
from upakarana.launcher import Launcher
from upakarana.models.commands import ModelCommands
from upakarana.views.list_view import AModelListView


class MainWindow(QMainWindow):
    def __init__(self, launcher: Launcher):
        super(MainWindow, self).__init__()

        self.app = App()
        self.app.events.emit("init", self)

        self.init_window()

        self.init_launcher(launcher)

        self.init_stacked_layout()

        # Command list view
        commands_content = QWidget()
        AModelListView(commands_content, ModelCommands, self.launcher.commands)
        self.stacked_layout.addWidget(commands_content)

    def init_window(self):
        # Disable window resizing
        self.setFixedSize(self.size())

        # Disable window moving
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Set the window size
        self.resize(800, 450)

        # Move the window to the center of the screen
        qtRectangle = self.frameGeometry()
        primary_screen = QGuiApplication.primaryScreen()
        if not primary_screen:
            raise Exception("Primary screen not found")

        centerPoint = primary_screen.availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Only hide the window if hotkeys are enabled
        if not self.app.is_hotkeys_disabled:
            # Hide the window initially
            self.hide()

            # Enable hotkeys
            HotKeys(self)

        self.app.events.emit("window_initialized", self)

    def init_stacked_layout(self):
        # Main Stacked Layout
        self.stacked_layout = QStackedLayout()
        self.app.stacked_layout = self.stacked_layout

        # Main Widget
        self.stacked_layout_widget = QWidget()
        self.stacked_layout_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(self.stacked_layout_widget)

        # Install the event filter
        self.installEventFilter(self)

    def init_launcher(self, launcher: Launcher):
        self.launcher = launcher
        self.app.events.emit("launcher_initialized", self.launcher)

        self.launcher.load_plugins()
        self.app.events.emit("plugins_loaded", self)

    # ℹ️ a0 is obj & a1 is event
    @override
    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a1 is None or a1.type() != QEvent.Type.KeyPress:
            return super().eventFilter(a0, a1)

        key_event = cast(QKeyEvent, a1)
        key: int = key_event.key()

        if key != Qt.Key.Key_Escape:
            return super().eventFilter(a0, a1)

        # If key is escape => go back to previous page
        layout_children_count = self.stacked_layout.count()
        layout_current_view_index = self.stacked_layout.currentIndex()
        if layout_children_count > 1:
            widget_to_remove = self.stacked_layout.currentWidget()
            self.stacked_layout.setCurrentIndex(layout_current_view_index - 1)
            self.stacked_layout.removeWidget(widget_to_remove)

        # If current page is last page => quit the app
        else:
            QApplication.quit()

        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow(Launcher())

    # assign main window to app instance
    _app = App()
    _app.is_hotkeys_disabled = "--hotkeys" not in sys.argv
    _app.main_window = w

    if _app.is_hotkeys_disabled:
        w.show()
    sys.exit(app.exec())
