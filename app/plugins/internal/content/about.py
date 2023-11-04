from PyQt6.QtWidgets import QLabel, QPushButton, QStackedLayout, QVBoxLayout, QWidget

from app.config import config


class AboutContent(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(QLabel(config.app_name))
        
        go_back_btn = QPushButton("Go back")
        go_back_btn.clicked.connect(self.go_back) # type: ignore
        layout.addWidget(go_back_btn)

        # self.content_widget = QWidget()
        self.setLayout(layout)

    def go_back(self):
        print("clicked...")
        # Auto select the first item in the list after filtering
        parent = self.parent()
        print(f"parent: {parent}")
        if isinstance(parent, QStackedLayout):
            print(f"parent.currentIndex(): {parent.currentIndex()}")
            parent.setCurrentIndex(parent.currentIndex() - 1)