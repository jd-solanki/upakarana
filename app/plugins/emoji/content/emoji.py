import json
import pathlib

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGridLayout, QLabel, QWidget

# Get current file directory
curr_dir = pathlib.Path(__file__).parent.resolve()

emoji_data = curr_dir / "emojis.json"

# Load emojis from json file
emojis = []
with open(emoji_data, "r") as file:
    emojis = json.load(file)


class EmojiContent(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()

        noto_fonts = QFont("Noto Color Emoji", 16)

        for i, emoji in enumerate(emojis):
            unicode_sequence = emoji["unicode"].encode("utf-8").decode("unicode_escape")
            emoji_text = QLabel(unicode_sequence)
            emoji_text.setFont(noto_fonts)
            layout.addWidget(emoji_text, i // 8, i % 8)

        self.setLayout(layout)
