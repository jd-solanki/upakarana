from abc import abstractmethod
from typing import Any, override

from PyQt6.QtCore import QAbstractListModel, QModelIndex
from PyQt6.QtWidgets import QListView


class AAbstractListModel[ListItem](QAbstractListModel):
    def __init__(
        self,
        list_items: list[ListItem],
        list_view: QListView,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.list_items: list[ListItem] = list_items
        self.filtered_list_items = list_items
        self.list_view = list_view

    def add_list_item(self, list_item: ListItem) -> None:
        # Calculate the new row index (which is the end of the list)
        new_row_index = self.rowCount()

        # Notify the view that a new row will be inserted at new_row_index
        self.beginInsertRows(QModelIndex(), new_row_index, new_row_index)
        self.list_items.append(list_item)  # Append the new item to the data list
        self.endInsertRows()  # End the row insertion process

        # Notify the view that the data has changed
        self.layoutChanged.emit()

    def move_item(self, from_index: int, to_index: int):
        if 0 <= from_index < self.rowCount() and 0 <= to_index < self.rowCount():
            # Swap the items
            self.list_items[from_index], self.list_items[to_index] = (
                self.list_items[to_index],
                self.list_items[from_index],
            )

            # Notify the view of the change
            self.dataChanged.emit(
                self.createIndex(min(from_index, to_index), 0),
                self.createIndex(max(from_index, to_index), 0),
            )

    def move_item_to_top(self, index: int):
        self.move_item(index, 0)

    @override
    def rowCount(self, parent: QModelIndex = QModelIndex()):
        return len(self.filtered_list_items)

    @abstractmethod
    def filter_list_item(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def on_select_item(self) -> None:
        raise NotImplementedError
