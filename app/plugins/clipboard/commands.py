from app.launcher import ContentCommand

from .content import ClipboardContent

clipboard = ContentCommand(name="Clipboard", content=ClipboardContent)
