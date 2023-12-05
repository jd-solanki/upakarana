from PyQt6.QtWidgets import QStackedLayout

from app.events import Events


class App:
    _instance = None
    stacked_layout: QStackedLayout = QStackedLayout()
    events: Events = Events()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls)
        return cls._instance
