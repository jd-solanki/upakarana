from typing import Any, Final, override

from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt6.QtWidgets import QListView, QMainWindow

from app.launcher import Command


class ModelCommands(QAbstractListModel):
    def __init__(self, commands: list[Command], list_view: QListView, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.MODEL_COMMANDS: Final[list[Command]] = commands
        self.filtered_commands = commands
        self.list_view = list_view

    @override
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            cmd = self.filtered_commands[index.row()]
            return cmd.name

    @override
    def rowCount(self, parent: QModelIndex = QModelIndex()):
        return len(self.filtered_commands)
    
    def get_command(self, index: QModelIndex) -> Command | None:
        if 0 <= index.row() < len(self.filtered_commands):
            return self.filtered_commands[index.row()]
        
        return None
    
    def filter_commands(self, text: str):
        if text:
            self.filtered_commands = [cmd for cmd in self.MODEL_COMMANDS if text.lower() in cmd.name.lower()]
        else:
            self.filtered_commands = self.MODEL_COMMANDS

        # notify the view that the data has changed
        self.layoutChanged.emit()

        # Auto select the first item in the list after filtering
        parent = self.parent()
        if isinstance(parent, QMainWindow):
            self.list_view.setCurrentIndex(self.index(0, 0))

    def execute_selected_command(self):
        # If there's no filtered commands => Don't do anything
        if not self.rowCount():
            return

        selected_item_index = self.list_view.currentIndex()
        command = self.get_command(selected_item_index)

        if command:
            command.execute()
        else:
            print("[ERROR] Can't find selected command")