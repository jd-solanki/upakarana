import subprocess
from typing import Callable, Iterable

from PyQt6.QtCore import QProcess, QTimer


def exec(command: list[str]):
    subprocess.run(command, shell=True, capture_output=True, text=True)


class CommandRunner:
    def __init__(
        self,
        program: str | None,
        arguments: Iterable[str | None],
        on_output: Callable[[str], None] = lambda x: None,
    ):
        self.program = program
        self.arguments = arguments
        self.on_output = on_output

        # Process
        self.p = None

    def exec_cmd(self):
        if self.p is None:
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)  # type: ignore
            self.p.start(self.program, self.arguments)
            self.p.finished.connect(self.on_finish)  # type:ignore

    def handle_stdout(self):
        if self.p:
            data = self.p.readAllStandardOutput()
            stdout = bytes(data).decode("utf8")  # type: ignore
            self.on_output(stdout)

    def on_err(self):
        if self.p:
            data = self.p.readAllStandardError()
            stderr = bytes(data).decode("utf8")  # type: ignore
            print(stderr)

    def on_finish(self):
        self.p = None


# Thanks: https://www.pythonguis.com/tutorials/pyqt6-qprocess-external-programs/
class IntervalCommand:
    def __init__(
        self,
        program: str | None,
        arguments: Iterable[str | None],
        timer_interval_in_ms: int = 1000,
        on_output: Callable[[str], None] = lambda x: None,
    ):
        self.program = program
        self.arguments = arguments

        self.cmd_runner = CommandRunner(
            self.program, self.arguments, on_output=on_output
        )

        self.timer = QTimer()
        self.timer.setInterval(
            timer_interval_in_ms
        )  # Check every `interval` milliseconds
        self.timer.timeout.connect(self.cmd_runner.exec_cmd)  # type: ignore
        self.timer.start()
