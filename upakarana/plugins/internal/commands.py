from upakarana.launcher import ContentCommand, ExecutableCommand

from .content.about import AboutContent


def exec_reload():
    print("Reloading Upakarana")


reload = ExecutableCommand(name="Reload Upakarana", execute=exec_reload)


about = ContentCommand(name="About", content=AboutContent)
