import sys
from typing import cast, override

from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedLayout, QWidget

from app.launcher import Launcher
from app.views.list_view import AListView


class MainWindow(QMainWindow):
    def __init__(self, launcher: Launcher):
        super(MainWindow, self).__init__()
        self.init_launcher(launcher)

        # Set window title
        self.setWindowTitle("Upakarana")
        self.init_stacked_layout()

        # Main list view
        AListView(self.launcher.commands, self.stacked_layout)

        # # Add main list view to stack
        # self.stacked_layout.addWidget(list_view.layout_widget)

    def init_stacked_layout(self):
        # Main Stacked Layout
        self.stacked_layout = QStackedLayout()

        # Main Widget
        stacked_layout_widget = QWidget()
        stacked_layout_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(stacked_layout_widget)

        # Install the event filter
        self.installEventFilter(self)

    def init_launcher(self, launcher: Launcher):
        self.launcher = launcher
        self.launcher.load_plugins()

    # ℹ️ a0 is obj & a1 is event
    @override
    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a1 is None or a1.type() != QEvent.Type.KeyPress:
            return super().eventFilter(a0, a1)

        key_event = cast(QKeyEvent, a1)
        key: int = key_event.key()
        if key != Qt.Key.Key_Escape:
            return super().eventFilter(a0, a1)

        if self.stacked_layout.currentIndex() > 0:
            self.stacked_layout.setCurrentIndex(self.stacked_layout.currentIndex() - 1)
        else:
            QApplication.quit()

        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow(Launcher())
    w.show()
    sys.exit(app.exec())
