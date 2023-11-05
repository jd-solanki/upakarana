from dataclasses import dataclass
from typing import override

from PyQt6.QtCore import QModelIndex, Qt

from app.models.abstract_list_model import AAbstractListModel


@dataclass
class ClipboardContent:
    content: str
    time: str


class ModelClipboard(AAbstractListModel[ClipboardContent]):
    @override
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            list_item = self.filtered_list_items[index.row()]
            return list_item.content
