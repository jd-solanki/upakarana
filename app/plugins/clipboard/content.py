from PyQt6.QtWidgets import QApplication, QWidget

from app.views.list_view import AModelListView

from .model import ClipboardItem, ModelClipboard


class ClipboardContent(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.clipboard_content: list[ClipboardItem] = []

        clipboard = QApplication.clipboard()

        if clipboard:
            self.clipboard = clipboard
        else:
            raise Exception("Clipboard not found")

        self.clipboard.dataChanged.connect(self.on_clipboard_change)  # type: ignore

        if self.clipboard.text():
            self.clipboard_content = [ClipboardItem(self.clipboard.text(), None)]

        self.model_list_view = AModelListView(ModelClipboard, self.clipboard_content)
        self.model = self.model_list_view.view_model

    def on_clipboard_change(self):
        self.model.add_list_item(ClipboardItem(self.clipboard.text(), None))
