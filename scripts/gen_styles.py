import sass

from upakarana.paths import css_dir, scss_dir

sass.compile(dirname=(str(scss_dir), str(css_dir)), output_style="compressed")
