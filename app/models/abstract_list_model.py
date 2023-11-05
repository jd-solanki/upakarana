from abc import ABC, abstractmethod
from typing import Any, Final, override

from PyQt6.QtCore import QAbstractListModel, QModelIndex
from PyQt6.QtWidgets import QListView, QStackedLayout


# We need to use this metaclass to avoid the following error: `TypeError: metaclass conflict: the metaclass of a derived class must be a`
class ABCQAbstractListModelMeta(type(QAbstractListModel), type(ABC)):
    pass


class AAbstractListModel[ListItem](
    ABC, QAbstractListModel, metaclass=ABCQAbstractListModelMeta
):
    def __init__(
        self,
        list_items: list[ListItem],
        list_view: QListView,
        stacked_layout: QStackedLayout,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.LIST_ITEMS: Final[list[ListItem]] = list_items
        self.filtered_list_items = list_items
        self.list_view = list_view
        self.stacked_layout = stacked_layout

    @override
    def rowCount(self, parent: QModelIndex = QModelIndex()):
        return len(self.filtered_list_items)

    @abstractmethod
    def filter_list_item(self, text: str):
        pass

    @abstractmethod
    def on_select_item(self):
        pass
