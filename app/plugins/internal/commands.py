from app.launcher import Command


def exec_reload():
        print("Reloading Upakarana")
reload = Command(name="Reload Upakarana", execute=exec_reload)
    


def exec_about():
    print(
        "This is upakarana. Cross platform python based launcher similar to Raycast & Script Kit."
    )
about = Command(name="About", execute=exec_about)
