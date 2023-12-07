"""Build a standalone executable using PyInstaller"""

from pathlib import Path

import PyInstaller.__main__

current_dir = Path(__file__).parent.resolve()
plugins_dir = current_dir / "app" / "plugins"


def generate_hidden_imports(plugin_dir: Path):
    hidden_imports: list[str] = []
    for dir in plugin_dir.glob("*"):
        if dir.is_dir():
            hidden_imports.append(f"--hidden-import=app.plugins.{dir.name}")
    return hidden_imports


current_dir = Path(__file__).parent.resolve()
plugins_dir = current_dir / "app" / "plugins"

hidden_imports = generate_hidden_imports(plugins_dir)

PyInstaller.__main__.run(
    [
        "--onefile",
        "--add-data",
        "app/plugins:app/plugins",
        *hidden_imports,
        "main.py",
    ]
)
