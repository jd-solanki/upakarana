import subprocess
from typing import Callable, Iterable

import httpx
from httpx import Response
from PyQt6.QtCore import QProcess, QTimer, pyqtBoundSignal
from PyQt6.QtWidgets import QLabel

from upakarana import App
from upakarana.worker import Worker


def exec(command: list[str]):
    subprocess.run(command, shell=True, capture_output=True, text=True)


class StatusBarMessage:
    def __init__(self):
        self.app = App()

        # Get current message
        self.w_label = self.app.status_bar.findChild(QLabel)
        self.prev_msg = self.w_label.text()
        print(f"self.prev_msg: {self.prev_msg}")

    def set(self, msg: str):
        self.w_label.setText(msg)

    def reset(self):
        self.w_label.setText(self.prev_msg)


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


class RequestHelper:
    def __init__(
        self,
        url: str,
        cb_res_handler: Callable[[Response], None],
        headers: dict[str, str] = {},
        params: dict[str, str] = {},
    ):
        self.url = url
        self.cb_res_handler = cb_res_handler
        self.headers = headers
        self.params = params
        self.app = App()

        # Meta
        self.is_loading = False
        self.data = None

    def run(self):
        worker = Worker(
            self.make_api_call
        )  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.cb_res_handler)  # type: ignore
        worker.signals.finished.connect(self.on_finish)  # type: ignore
        # worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.app.threadpool.start(worker)

    def make_api_call(self, progress_callback: pyqtBoundSignal) -> Response:
        self.is_loading = True

        # Make API call
        # TODO: Handle exceptions & errors
        r = httpx.get(self.url, headers=self.headers, params=self.params)
        progress_callback.emit(100)
        return r

    # def handle_response(self, r: Response):
    #     self.data = r.json()

    def on_finish(self):
        print("THREAD COMPLETE!")
        self.is_loading = False
