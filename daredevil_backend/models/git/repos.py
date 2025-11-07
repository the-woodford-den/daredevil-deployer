"""Git Repo Typed Models"""

from typing import Optional

from pydantic import AliasGenerator, ConfigDict, EmailStr
from sqlmodel import Field, SQLModel

from models import IDModel, TSModel
from utility import serialize


class RepositoryBase(SQLModel):
    node_id: Optional[str]
    name: Optional[str]
    full_name: Optional[str]
    private: Optional[bool]
    html_url: Optional[str]
    description: Optional[str]
    fork: Optional[bool]
    url: Optional[str]
    archive_url: Optional[str]
    assignees_url: Optional[str]
    blobs_url: Optional[str]
    branches_url: Optional[str]
    collaborators_url: Optional[str]
    comments_url: Optional[str]
    commits_url: Optional[str]
    compare_url: Optional[str]
    contents_url: Optional[str]
    contributors_url: Optional[str]
    deployments_url: Optional[str]
    downloads_url: Optional[str]
    events_url: Optional[str]
    forks_url: Optional[str]
    git_commits_url: Optional[str]
    git_refs_url: Optional[str]
    git_tags_url: Optional[str]
    git_url: Optional[str]
    issue_comment_url: Optional[str]
    issue_events_url: Optional[str]
    issues_url: Optional[str]
    keys_url: Optional[str]
    labels_url: Optional[str]
    languages_url: Optional[str]
    merges_url: Optional[str]
    milestones_url: Optional[str]
    notifications_url: Optional[str]
    pulls_url: Optional[str]
    releases_url: Optional[str]
    ssh_url: Optional[str]
    stargazers_url: Optional[str]
    statuses_url: Optional[str]
    subscribers_url: Optional[str]
    subscription_url: Optional[str]
    tags_url: Optional[str]
    teams_url: Optional[str]
    trees_url: Optional[str]
    clone_url: Optional[str]
    mirror_url: Optional[str] = Field(default=None)
    hooks_url: Optional[str]
    svn_url: Optional[str]
    homepage: Optional[str] = Field(default=None)
    language: Optional[str]
    forks_count: Optional[int]
    stargazers_count: Optional[int]
    watchers_count: Optional[int]
    size: Optional[int]
    default_branch: Optional[str]
    open_issues_count: Optional[int]
    is_template: Optional[bool]
    has_issues: Optional[bool]
    has_projects: Optional[bool]
    has_wiki: Optional[bool]
    has_pages: Optional[bool]
    has_downloads: Optional[bool]
    archived: Optional[bool]
    disabled: Optional[bool]
    visibility: Optional[str]
    pushed_at: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    allow_rebase_merge: Optional[bool] = Field(default=False)
    template_repository: Optional[str] = Field(default=None)
    temp_clone_token: Optional[str] = Field(default=None)
    allow_squash_merge: Optional[bool] = Field(default=False)
    allow_auto_merge: Optional[bool] = Field(default=False)
    delete_branch_on_merge: Optional[bool] = Field(default=False)
    allow_merge_commit: Optional[bool] = Field(default=False)
    subscribers_count: Optional[int] = Field(default=0)
    network_count: Optional[int] = Field(default=0)
    forks: Optional[int] = Field(default=0)
    open_issues: Optional[int] = Field(default=0)
    watchers: Optional[int] = Field(default=0)


class RepositoryOwnerResponse(SQLModel):
    id: int
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    login: str
    node_id: str
    avatar_url: str
    gravatar_id: Optional[str] = Field(default=None)
    url: str = Field()
    html_url: str = Field()
    followers_url: str = Field()
    following_url: str = Field()
    gists_url: str = Field()
    starred_url: str = Field()
    subscriptions_url: str = Field()
    organizations_url: str = Field()
    repos_url: str = Field()
    events_url: str = Field()
    received_events_url: str = Field()
    type: str = Field()
    user_view_type: str = Field()
    site_admin: bool = Field(default=False)


class RepositoryPermissionsResponse(SQLModel):
    admin: bool = Field()
    push: bool = Field()
    pull: bool = Field()
    maintain: bool = Field()
    triage: bool = Field()


class RepositoryLicenseResponse(SQLModel):
    key: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    url: Optional[str] = Field(default=None)
    spdx_id: Optional[str] = Field(default=None)
    node_id: Optional[str] = Field(default=None)
    html_url: Optional[str] = Field(default=None)


class RepositoryResponse(RepositoryBase):
    topics: list[Optional[str]] = Field()
    owner: Optional[RepositoryOwnerResponse] = Field()
    license: Optional[RepositoryLicenseResponse] = Field()
    permissions: Optional[RepositoryPermissionsResponse] = Field()
    id: int = Field()


class Repository(RepositoryBase, IDModel, TSModel, table=True):
    __tablename__ = "git_repos"
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=lambda field_name: (serialize(field_name))
        )
    )
    git_id: int = Field()


#
