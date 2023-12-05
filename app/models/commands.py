from typing import override

from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtWidgets import QMainWindow

from app import App
from app.launcher import ContentCommand, ExecutableCommand
from app.models.abstract_list_model import AAbstractListModel


class ModelCommands(AAbstractListModel[ContentCommand | ExecutableCommand]):
    @override
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            list_item = self.filtered_list_items[index.row()]
            return list_item.name

    def get_command(
        self, index: QModelIndex
    ) -> ExecutableCommand | ContentCommand | None:
        if 0 <= index.row() < len(self.filtered_list_items):
            return self.filtered_list_items[index.row()]

        return None

    def filter_list_item(self, text: str):
        if text:
            self.filtered_list_items = [
                list_item
                for list_item in self.list_items
                if text.lower() in list_item.name.lower()
            ]
        else:
            self.filtered_list_items = self.list_items

        # notify the view that the data has changed
        self.layoutChanged.emit()

        # Auto select the first item in the list after filtering
        parent = self.parent()
        if isinstance(parent, QMainWindow):
            self.list_view.setCurrentIndex(self.index(0, 0))

    def on_select_item(self):
        # If there's no filtered commands => Don't do anything
        if not self.rowCount():
            return

        selected_item_index = self.list_view.currentIndex()
        command = self.get_command(selected_item_index)

        if command:
            if isinstance(command, ExecutableCommand):
                command.execute()
            if isinstance(command, ContentCommand):
                stacked_layout = App().stacked_layout
                stacked_layout.addWidget(command.content())
                stacked_layout.setCurrentIndex(stacked_layout.currentIndex() + 1)
        else:
            print("[ERROR] Can't find selected command")
