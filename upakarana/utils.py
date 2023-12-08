import subprocess

from PyQt6.QtCore import QThread, pyqtSignal


class CommandRunner(QThread):
    output = pyqtSignal(str)

    def __init__(self, command: list[str]):
        super().__init__()
        self.command = command

    def run(self):
        result = subprocess.run(
            self.command, shell=True, capture_output=True, text=True
        )
        self.output.emit(result.stdout)
