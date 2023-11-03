import importlib
import pathlib
from dataclasses import dataclass
from typing import Callable

current_dir = pathlib.Path(__file__).parent.resolve()
plugins_dir = current_dir / "plugins"


@dataclass
class Command:
    name: str
    execute: Callable[[], None]

@dataclass
class Plugin:
    name: str
    init: Callable[["Launcher"], None]


class Launcher:
    def __init__(self):
        self.plugins: list[Plugin] = []
        self.commands: list[Command] = []

    def register_plugin(self, plugin: Plugin) -> None:
        self.plugins.append(plugin)

    def register_commands(self, command: Command) -> None:
        self.commands.append(command)

    def load_plugins(self) -> None:
        # Get list of plugin directories
        plugin_dirs = [path for path in plugins_dir.iterdir() if path.is_dir()]

        # plugins = [importlib.import_module(f'app.plugins.{dir.name}') for dir in plugin_dirs]

        for dir in plugin_dirs:
            plugin_module = importlib.import_module(f"app.plugins.{dir.name}")
            self.plugins.append(plugin_module.Plugin)
            plugin_module.Plugin.init(self)