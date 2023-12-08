import platform
from pathlib import Path
from typing import Literal

type Platforms = Literal["windows", "linux", "darwin"]


class PlatformUtils:
    def get_platform(self) -> Platforms:
        return platform.system().lower()  # type: ignore

    def get_platform_app_dir(self) -> Path:
        """Return platform specific app directory for storing data like settings, images, etc."""
        platform = self.get_platform()

        if platform == "linux":
            return Path.home() / ".config"
        elif platform == "windows":
            return Path.home() / "AppData" / "Local"
        elif platform == "darwin":
            return Path.home() / "Library" / "Application Support"
        else:
            raise Exception(
                "Platform not supported. Supported platforms: windows, linux, darwin"
            )
