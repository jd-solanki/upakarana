
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

    def init_launcher(self, launcher: Launcher):
        self.launcher = launcher
        self.launcher.load_plugins()

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow(Launcher())
    w.show()
    app.exec()