from typing import Final

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListView, QVBoxLayout, QWidget

from app.custom_widgets.line_edit import ModelFilterLineEdit
from app.launcher import Command
from app.models.commands import ModelCommands


class AListView():
    def __init__(self, commands: list[Command]):
        self.VIEW_COMMANDS: Final[list[Command]] = commands
        self.init_ui()

    def init_ui(self):
        # Views
        self.list_view = QListView()

        # Models
        self.commands_model = ModelCommands(self.VIEW_COMMANDS, self.list_view)

        layout = QVBoxLayout()

        # Line Edit
        line_edit = ModelFilterLineEdit(self.list_view)
        line_edit.setPlaceholderText("Search command...")
        line_edit.textChanged.connect(self.commands_model.filter_commands) # type: ignore
        line_edit.returnPressed.connect(self.commands_model.execute_selected_command) # type: ignore

        layout.addWidget(line_edit)

        # List
        self.list_view.setModel(self.commands_model)

        # Execute command on click of list item
        self.list_view.clicked.connect(self.commands_model.execute_selected_command)  # type: ignore

        # prevent QListView from taking focus when we click on list item to execute the command.
        # If we don't do this, after clicking we navigate to another list item and press return that command won't get executed because only line edit has `returnPressed` signal that can execute command when enter/return is pressed.
        # In addition to this issue, We have to focus line edit again to type.
        self.list_view.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # Auto select first list item on init
        self.list_view.setCurrentIndex(self.commands_model.index(0, 0))

        layout.addWidget(self.list_view)

        # Main Widget
        self.layout_widget = QWidget()
        self.layout_widget.setLayout(layout)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)