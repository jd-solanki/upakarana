import webbrowser
from typing import TypedDict, override

from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtWidgets import QMainWindow

from upakarana.models.abstract_list_model import AAbstractListModel


class Repository(TypedDict):
    name: str
    full_name: str
    private: bool
    html_url: str
    owner: dict[str, str]


class ModelGithubRepositories(AAbstractListModel[Repository]):
    @override
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            list_item = self.filtered_list_items[index.row()]
            return list_item.get("full_name")

    def get_item(self, index: QModelIndex) -> Repository | None:
        if 0 <= index.row() < len(self.filtered_list_items):
            return self.filtered_list_items[index.row()]

        return None

    def does_item_exist(self, content: str) -> bool:
        return any(content == item.get("name") for item in self.list_items)

    @override
    def on_select_item(self):
        # If there's no filtered commands => Don't do anything
        if not self.rowCount():
            return

        selected_item_index = self.list_view.currentIndex()
        item = self.get_item(selected_item_index)

        if item:
            webbrowser.open(item.get("html_url"))

    @override
    def filter_list_item(self, text: str):
        if text:
            self.filtered_list_items = [
                list_item
                for list_item in self.list_items
                if text.lower() in list_item.get("name").lower()
            ]
        else:
            self.filtered_list_items = self.list_items

        # notify the view that the data has changed
        self.layoutChanged.emit()

        # Auto select the first item in the list after filtering
        parent = self.parent()
        if isinstance(parent, QMainWindow):
            self.list_view.setCurrentIndex(self.index(0, 0))
