from typing import TypedDict, cast, override

from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QClipboard
from PyQt6.QtWidgets import QMainWindow

from app import App
from app.models.abstract_list_model import AAbstractListModel


class ClipboardItem(TypedDict):
    content: str
    time: str | None


class ModelClipboard(AAbstractListModel[ClipboardItem]):
    @override
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            list_item = self.filtered_list_items[index.row()]
            return list_item.get("content")

    def get_clipboard_item(self, index: QModelIndex) -> ClipboardItem | None:
        if 0 <= index.row() < len(self.filtered_list_items):
            return self.filtered_list_items[index.row()]

        return None

    def does_item_exist(self, content: str) -> bool:
        return any(content == item.get("content") for item in self.list_items)

    @override
    def on_select_item(self):
        # If there's no filtered commands => Don't do anything
        if not self.rowCount():
            return

        selected_item_index = self.list_view.currentIndex()
        clipboard_item = self.get_clipboard_item(selected_item_index)

        if clipboard_item:
            app = App()
            clipboard = cast(QClipboard, app._clipboard_handler.clipboard)  # type: ignore

            clipboard.blockSignals(True)
            clipboard.setText(clipboard_item.get("content"))
            clipboard.blockSignals(False)

            # Move the item to the top
            self.move_item_to_top(selected_item_index.row())
            self.list_view.setCurrentIndex(
                self.index(0, 0)
            )  # Set the selected item to the first index

    @override
    def filter_list_item(self, text: str):
        if text:
            self.filtered_list_items = [
                list_item
                for list_item in self.list_items
                if text.lower() in list_item.get("content").lower()
            ]
        else:
            self.filtered_list_items = self.list_items

        # notify the view that the data has changed
        self.layoutChanged.emit()

        # Auto select the first item in the list after filtering
        parent = self.parent()
        if isinstance(parent, QMainWindow):
            self.list_view.setCurrentIndex(self.index(0, 0))
