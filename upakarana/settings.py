import json
from pathlib import Path
from typing import Any

from upakarana.config import config
from upakarana.platform import PlatformUtils

type TypeSettings = dict[str, Any]


class Settings:
    def __init__(self):
        self.platform_utils = PlatformUtils()

        self.data_dir = self.platform_utils.get_platform_app_dir() / config.app_name
        self.ensure_data_dir_exists()

    def ensure_data_dir_exists(self):
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True)

    @property
    def settings_file_path(self) -> Path:
        return self.data_dir / "settings.json"

    @property
    def _settings(self) -> TypeSettings:
        json_str = self.settings_file_path.read_text()
        return json.loads(json_str)

    @_settings.setter
    def _settings(self, value: TypeSettings):
        self.settings_file_path.write_text(json.dumps(value, indent=4))

    def get(self, key: str, fallback: Any = None) -> Any:
        return self._settings.get(key, fallback)

    def set(self, key: str, value: Any) -> None:
        self._settings[key] = value


class PluginSettings(Settings):
    def __init__(self, plugin_name: str):
        super().__init__()
        self.plugin_name = plugin_name
        self.data_dir = self.data_dir / "plugins" / plugin_name

        # ℹ️ As we changed the data_dir, we need to ensure it exists again
        self.ensure_data_dir_exists()
