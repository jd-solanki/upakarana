from pathlib import Path

from PyQt6.QtGui import QFont, QFontDatabase


class CustomFont:
    def __init__(self, font_dir: Path):
        # Add each font file in the directory
        for font_file in font_dir.glob("*.ttf"):
            QFontDatabase.addApplicationFont(str(font_file))

    def get_font(self, font_name: str, font_size: int) -> QFont:
        for family in QFontDatabase.families():
            if font_name in family:
                return QFont(family, font_size)

        # Return default fonts if font not found
        print(f"[WARN] Font not found: {font_name}")
        return QFont()
