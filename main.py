from typing import Any, override

from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QListView,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from app.launcher import Command, Launcher


class MyLineEdit(QLineEdit):
    def __init__(self, list_view: QListView, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.list_view = list_view

    # ℹ️ a0 is event
    @override
    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        if not a0:
            return

        super().keyPressEvent(a0)
        list_view_model = self.list_view.model()

        if isinstance(list_view_model, ModelCommands):
            if a0.key() == Qt.Key.Key_Up:
                current_index = self.list_view.currentIndex().row()
                if current_index > 0:
                    self.list_view.setCurrentIndex(list_view_model.index(current_index - 1, 0))
            elif a0.key() == Qt.Key.Key_Down:
                current_index = self.list_view.currentIndex().row()
                if current_index < list_view_model.rowCount() - 1:
                    self.list_view.setCurrentIndex(list_view_model.index(current_index + 1, 0))


class MainWindow(QMainWindow):

    def __init__(self, launcher: Launcher):
        super(MainWindow, self).__init__()
        self.init_launcher(launcher)

        # Models
        self.commands_model = ModelCommands(self.launcher)

        # Views
        self.list_view = QListView()


        self.setWindowTitle("My App")

        layout = QVBoxLayout()

        # Line Edit
        line_edit = MyLineEdit(self.list_view)
        line_edit.setPlaceholderText("Search...")
        line_edit.textChanged.connect(self.commands_model.filter_commands) # type: ignore
        line_edit.returnPressed.connect(self.execute_selected_command) # type: ignore

        layout.addWidget(line_edit)

        # List
        self.list_view.setModel(self.commands_model)
        
        # Auto select first list item on init
        self.list_view.setCurrentIndex(self.commands_model.index(0, 0))

        layout.addWidget(self.list_view)

        # Main Widget
        widget = QWidget()
        widget.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setCentralWidget(widget)

    def execute_selected_command(self):
        # If there's no filtered commands => Don't do anything
        if not self.commands_model.rowCount():
            return

        selected_item_index = self.list_view.currentIndex()
        command = self.commands_model.get_command(selected_item_index)

        if command:
            command.execute()
        else:
            print("[ERROR] Can't find selected command")

    def init_launcher(self, launcher: Launcher):
        self.launcher = launcher
        self.launcher.load_plugins()

class ModelCommands(QAbstractListModel):
    def __init__(self, launcher: Launcher, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.launcher = launcher
        self.commands: list[Command] = launcher.commands

    @override
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            cmd = self.commands[index.row()]
            return cmd.name

    @override
    def rowCount(self, parent: QModelIndex = QModelIndex()):
        return len(self.commands)
    
    def get_command(self, index: QModelIndex) -> Command | None:
        if 0 <= index.row() < len(self.commands):
            return self.commands[index.row()]
        
        return None
    
    def filter_commands(self, text: str):
        if text:
            self.commands = [cmd for cmd in self.launcher.commands if text.lower() in cmd.name.lower()]
        else:
            self.commands = self.launcher.commands

        # notify the view that the data has changed
        self.layoutChanged.emit()

        # Auto select the first item in the list after filtering
        parent = self.parent()
        if isinstance(parent, MainWindow):
            parent.list_view.setCurrentIndex(self.index(0, 0))

if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow(Launcher())
    w.show()
    app.exec()