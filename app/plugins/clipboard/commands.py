from app.launcher import ContentCommand

from .content.clipboard import ClipboardContent

clipboard = ContentCommand(name="Clipboard", content=ClipboardContent)
