from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class EmojiContent(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        emoji_text = QLabel("\U0001F923 \U0001F602 \U0001F609")

        noto_fonts = QFont("Noto Color Emoji", 16)

        emoji_text.setFont(noto_fonts)
        layout.addWidget(emoji_text)

        self.setLayout(layout)
