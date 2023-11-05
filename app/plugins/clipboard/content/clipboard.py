from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ClipboardContent(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        label = QLabel("Hi, I'm Clipboard")
        layout.addWidget(label)

        self.setLayout(layout)

    def on_clipboard_change(self):
        ...
