from typing import cast

from PyQt6.QtWidgets import QWidget

from app import App
from app.views.list_view import AModelListView

from .model import ModelClipboard
from .service import ClipboardHandler


class ClipboardContent(QWidget):
    def __init__(self) -> None:
        super().__init__()

        app = App()
        self.clipboard_handler = cast(ClipboardHandler, app._clipboard_handler)  # type: ignore
        self.clipboard_watcher = self.clipboard_handler.clipboard_watcher

        self.model_list_view = AModelListView(
            self, ModelClipboard, self.clipboard_handler.get_clipboard_content()
        )

        # TODO: Improve type of `AModelListView` to get rid of this cast
        self.model = cast(ModelClipboard, self.model_list_view.view_model)

        self.clipboard_watcher.clipboard_changed.connect(self.on_clipboard_change)  # type: ignore

    # TODO: We can move this to model
    def on_clipboard_change(self, new_clipboard_content: str):
        if (
            not self.model.does_item_exist(new_clipboard_content)
            and new_clipboard_content
        ):
            self.model.add_list_item(
                {"content": new_clipboard_content, "time": None}, index=0
            )
