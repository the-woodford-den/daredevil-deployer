from typing import List, Optional

from .base import IDModel, TSModel


class GithubRepoRead(IDModel, TSModel):
    name: str


class GithubUserRead(IDModel, TSModel):
    login: str
    github_id: int
    avatar_url: str
    gravatar_id: Optional[int]
    api_url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    organizations_url: str
    repos_url: str
    site_admin: bool


class GithubBase(IDModel, TSModel):
    user: GithubUserRead
    repos: List[GithubRepoRead]
