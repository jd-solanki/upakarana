from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from app.config import config


class AboutContent(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        app_label = QLabel("👨‍💻 " + config.app_name.capitalize())
        font = app_label.font()
        font.setPointSize(16)
        app_label.setFont(font)
        layout.addWidget(app_label)

        app_desc = QLabel(config.app_desc)
        layout.addWidget(app_desc)

        self.setLayout(layout)
