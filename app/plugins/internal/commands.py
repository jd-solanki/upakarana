from app.launcher import ContentCommand, ExecutableCommand

from .content.about import AboutContent


def exec_reload():
        print("Reloading Upakarana")
reload = ExecutableCommand(name="Reload Upakarana", execute=exec_reload)
    


def exec_about():
    print(
        "This is upakarana. Cross platform python based launcher similar to Raycast & Script Kit."
    )
about = ContentCommand(name="About", content=AboutContent)
