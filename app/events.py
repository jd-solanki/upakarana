from typing import Any, Callable, TypedDict

# TODO: Improve typing


class Event(TypedDict):
    event: str
    callback: Callable[..., Any]


class Events:
    def __init__(self) -> None:
        self.events: list[Event] = []

    def on(self, event: str, callback: Callable[..., Any]):
        self.events.append({"event": event, "callback": callback})

    def emit(self, event: str, *args: Any, **kwargs: Any):
        for e in self.events:
            if e["event"] == event:
                e["callback"](*args, **kwargs)
