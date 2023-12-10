from typing import cast

from httpx import Response
from PyQt6.QtWidgets import QWidget

from upakarana.utils import RequestHelper
from upakarana.views.list_view import AModelListView

from .model import ModelGithubRepositories, Repository


class RepositoriesListContent(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.repositories: list[Repository] = []
        self.model_list_view = AModelListView(
            self,
            ModelGithubRepositories,
            self.repositories,
            search_placeholder="Search repositories...",
        )
        self.fetch_repos()

        # TODO: Improve type of `AModelListView` to get rid of this cast
        self.model = cast(ModelGithubRepositories, self.model_list_view.view_model)

        # Listen for line edit text change
        # self.model_list_view.line_edit.debounced_text_changed.connect(self.fetch_repos)  # type: ignore
        self.model_list_view.line_edit.debounced_text_changed.connect(self.fetch_repos)  # type: ignore

    def fetch_repos(self):
        _search_url = "https://api.github.com/search/repositories"
        _list_url = "https://api.github.com/user/repos"

        url = _list_url
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer <YOUR_TOKEN>",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        params = {
            "affiliation": "owner,collaborator",
            "sort": "updated",
        }

        line_edit_text = self.model_list_view.line_edit.text()
        if line_edit_text:
            url = _search_url

            # Add repo owner to search query
            params["q"] = line_edit_text + " owner:<YOUR_USERNAME>"
        else:
            url = _list_url
            params["q"] = ""

        RequestHelper(url, self.on_response, headers=headers, params=params).run()

    def on_response(self, r: Response):
        # Check if response is list or dict
        is_list_res = isinstance(r.json(), list)
        # update model

        self.repositories = r.json() if is_list_res else r.json().get("items", [])

        self.model.list_items = self.repositories
        self.model.filtered_list_items = self.repositories
        self.model.layoutChanged.emit()
