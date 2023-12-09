from upakarana.launcher import ContentCommand

from .content import RepositoriesListContent

repositories = ContentCommand(
    name="GitHub Repositories", content=RepositoriesListContent
)
