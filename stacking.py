import sys
from typing import cast, override

from PyQt6.QtCore import QEvent, QObject, Qt
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super(MainWindow, self).__init__()

        # Create a QVBoxLayout
        layout_1 = QVBoxLayout()
        layout_2 = QVBoxLayout()

        # Create a QPushButton and add it to the QVBoxLayout
        go_in_btn = QPushButton("Go In")
        go_in_btn.clicked.connect(lambda _: self.stacked_layout.setCurrentIndex(1))  # type: ignore
        layout_1.addWidget(go_in_btn)

        go_out_btn = QPushButton("Go Out")
        go_out_btn.clicked.connect(lambda _: self.stacked_layout.setCurrentIndex(0))  # type: ignore
        layout_2.addWidget(go_out_btn)

        # Create a QWidget and set its layout to the QVBoxLayout
        layout_1_widget = QWidget()
        layout_1_widget.setLayout(layout_1)

        layout_2_widget = QWidget()
        layout_2_widget.setLayout(layout_2)

        # Create a QStackedLayout
        self.stacked_layout = QStackedLayout()

        # Add the QWidget to the QStackedLayout
        self.stacked_layout.addWidget(layout_1_widget)
        self.stacked_layout.addWidget(layout_2_widget)

        self.stacked_layout.setCurrentIndex(0)

        # Main Widget
        stacked_layout_widget = QWidget()
        stacked_layout_widget.setLayout(self.stacked_layout)
        self.setCentralWidget(stacked_layout_widget)

        # Install the event filter
        self.installEventFilter(self)

    # ℹ️ a0 is obj & a1 is event
    @override
    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a1 is None or a1.type() != QEvent.Type.KeyPress:
            return super().eventFilter(a0, a1)

        key_event = cast(QKeyEvent, a1)
        key: int = key_event.key()
        if key != Qt.Key.Key_Escape:
            return super().eventFilter(a0, a1)

        if self.stacked_layout.currentIndex() > 0:
            self.stacked_layout.setCurrentIndex(self.stacked_layout.currentIndex() - 1)
        else:
            QApplication.quit()

        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
