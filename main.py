
from PyQt6.QtWidgets import QApplication, QMainWindow

from app.launcher import Launcher
from app.views.list_view import AListView


class MainWindow(QMainWindow):

    def __init__(self, launcher: Launcher):
        super(MainWindow, self).__init__()
        self.init_launcher(launcher)

        # Set window title
        self.setWindowTitle("Upakarana")

        list_view = AListView(self.launcher.commands)

        self.setCentralWidget(list_view.layout_widget)

    def init_launcher(self, launcher: Launcher):
        self.launcher = launcher
        self.launcher.load_plugins()

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow(Launcher())
    w.show()
    app.exec()