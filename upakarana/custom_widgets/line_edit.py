from typing import Any, override

from PyQt6.QtCore import QAbstractItemModel, QObject, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QLineEdit,
    QListView,
)


class CustomSignals(QObject):
    debounced_text_changed = pyqtSignal(str)


class ModelFilterLineEdit(QLineEdit):
    def __init__(self, list_view: QListView, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.list_view = list_view

        self._custom_signals = CustomSignals()
        self.debounced_text_changed = self._custom_signals.debounced_text_changed

        # TODO: Extract this to a separate class
        # TODO: Document this
        self.debounce = QTimer()
        self.debounce.setInterval(500)
        self.debounce.setSingleShot(True)
        self.debounce.timeout.connect(  # type: ignore
            lambda: self.debounced_text_changed.emit(self.text())
        )
        self.textChanged.connect(self.debounce.start)  # type: ignore

    # ℹ️ a0 is event
    @override
    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        if not a0:
            return

        super().keyPressEvent(a0)
        list_view_model = self.list_view.model()

        if isinstance(list_view_model, QAbstractItemModel):
            if a0.key() == Qt.Key.Key_Up:
                current_index = self.list_view.currentIndex().row()
                if current_index > 0:
                    self.list_view.setCurrentIndex(
                        list_view_model.index(current_index - 1, 0)
                    )
            elif a0.key() == Qt.Key.Key_Down:
                current_index = self.list_view.currentIndex().row()
                if current_index < list_view_model.rowCount() - 1:
                    self.list_view.setCurrentIndex(
                        list_view_model.index(current_index + 1, 0)
                    )
