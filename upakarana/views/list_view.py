from typing import Final, Type

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListView, QVBoxLayout, QWidget

from upakarana import App
from upakarana.custom_widgets.line_edit import ModelFilterLineEdit
from upakarana.models.abstract_list_model import AAbstractListModel


class AModelListView[ListItem]:
    def __init__(
        self,
        parent_widget: QWidget,
        model: Type[AAbstractListModel[ListItem]],
        list_items: list[ListItem],
    ):
        self.app = App()
        self.parent = parent_widget
        self.model = model
        self.VIEW_ITEMS: Final[list[ListItem]] = list_items
        self.init_ui()

    def init_ui(self):
        # Views
        self.list_view = QListView()
        self.app.set_font(self.list_view)

        # Models
        self.view_model = self.model(self.VIEW_ITEMS, self.list_view)

        # Line Edit
        self.line_edit = ModelFilterLineEdit(self.list_view)
        self.line_edit.setPlaceholderText("Search command...")
        self.line_edit.textChanged.connect(self.view_model.filter_list_item)  # type: ignore
        self.line_edit.returnPressed.connect(self.view_model.on_select_item)  # type: ignore

        # List
        self.list_view.setModel(self.view_model)

        # Execute command on click of list item
        self.list_view.clicked.connect(self.view_model.on_select_item)  # type: ignore

        # prevent QListView from taking focus when we click on list item to execute the command.
        # If we don't do this, after clicking we navigate to another list item and press return that command won't get executed because only line edit has `returnPressed` signal that can execute command when enter/return is pressed.
        # In addition to this issue, We have to focus line edit again to type.
        self.list_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Auto select first list item on init
        self.list_view.setCurrentIndex(self.view_model.index(0, 0))

        self.add_widgets_to_layout()

    def add_widgets_to_layout(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)

        layout.addWidget(self.line_edit)

        layout.addWidget(self.list_view)
        layout.setContentsMargins(0, 0, 0, 0)

        # Main Widget
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.parent.setLayout(layout)
