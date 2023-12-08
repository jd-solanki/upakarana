from pathlib import Path

pkg_dir = Path(__file__).parent.resolve()
repo_root = pkg_dir.parent

plugins_dir = pkg_dir / "plugins"

# Fonts
fonts_dir = pkg_dir / "fonts"

# Styles
styles_dir = pkg_dir / "styles"
scss_dir = styles_dir / "scss"
css_dir = styles_dir / "dist"
