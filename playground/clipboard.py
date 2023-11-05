import datetime
import sys
from typing import List, Tuple

from PyQt6.QtCore import QAbstractListModel, QModelIndex, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListView,
    QMainWindow,
    QWidget,
)


class ClipboardModel(QAbstractListModel):
    def __init__(self, data: List[Tuple[str, str]], parent=None):
        super().__init__(parent)
        self._data = data

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            text, timestamp = self._data[index.row()]
            return f"{timestamp}: {text}"


class ClipboardContent(QWidget):
    def __init__(self):
        super().__init__()

        # Create a QHBoxLayout
        layout = QHBoxLayout()

        # Create a QListView for the clipboard history
        self.clipboard_list_view = QListView()
        layout.addWidget(self.clipboard_list_view, 40)  # 40% width

        # Create a QLabel for the clipboard content preview
        self.clipboard_content_label = QLabel()
        layout.addWidget(self.clipboard_content_label, 60)  # 60% width

        # Set the layout
        self.setLayout(layout)

        # Connect to the clipboard data changed signal
        QApplication.clipboard().dataChanged.connect(self.update_clipboard_history)

        # Initialize the clipboard history
        self.clipboard_history: List[
            Tuple[str, str]
        ] = []  # Each item is a tuple of (content, timestamp)

        # Initialize the model
        self.model = ClipboardModel(self.clipboard_history)
        self.clipboard_list_view.setModel(self.model)

    def update_clipboard_history(self):
        print("Updating clipboard history")
        # Get the current clipboard content
        clipboard = QApplication.clipboard()
        current_content = clipboard.text()

        # Ignore if the clipboard is empty
        if not current_content:
            return

        if self.clipboard_history:
            # Ignore if the clipboard content is same as the last item in the history
            if self.clipboard_history[-1][0] == current_content:
                return

        # Get the current timestamp
        current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Add the current content and timestamp to the history
        self.clipboard_history.insert(0, (current_content, current_timestamp))

        # Update the QListView and QLabel
        self.model.layoutChanged.emit()
        self.update_clipboard_content_label()

    def update_clipboard_content_label(self):
        # Update the QLabel with the current clipboard content
        self.clipboard_content_label.setText(
            self.clipboard_history[0][0] if self.clipboard_history else ""
        )


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        widget = ClipboardContent()
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
