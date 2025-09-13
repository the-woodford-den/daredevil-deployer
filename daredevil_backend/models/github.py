from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .base import IDModel, TSModel
from .user import User


class RepoOwnerBase(SQLModel):
    login: str
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    user_view_type: str
    site_admin: bool


class RepoOwnerResponse(RepoOwnerBase):
    id: int


class RepoOwner(RepoOwnerBase, IDModel, TSModel):  # , table=True):
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="github")


class RepoPermissionBase(SQLModel):
    admin: bool
    push: bool
    pull: bool
    maintain: bool
    triage: bool


class RepoPermission(RepoPermissionBase, IDModel, TSModel):  # , table=True):
    repository: "Repository" = Relationship(back_populates="permission")
    repository_id: int = Field(foreign_key="repository.id")
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="repo_permissions")


class RepositoryBase(SQLModel):
    node_id: Optional[str]
    name: Optional[str]
    full_name: Optional[str]
    owner: Optional[RepoOwnerResponse]
    private: Optional[bool]
    html_url: Optional[str]
    description: Optional[str] | None
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
    mirror_url: Optional[str] | None
    hooks_url: Optional[str]
    svn_url: Optional[str]
    homepage: Optional[str] | None
    language: Optional[str]
    forks_count: Optional[int]
    stargazers_count: Optional[int]
    watchers_count: Optional[int]
    size: Optional[int]
    default_branch: Optional[str]
    open_issues_count: Optional[int]
    is_template: Optional[bool]
    topics: List[Optional[str]]
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
    permissions: Optional[RepoPermissionBase]
    allow_rebase_merge: Optional[bool] | None = False
    template_repository: Optional[str] | None = None
    temp_clone_token: Optional[str] | None = None
    allow_squash_merge: Optional[bool] | None = False
    allow_auto_merge: Optional[bool] | None = False
    delete_branch_on_merge: Optional[bool] | None = False
    allow_merge_commit: Optional[bool] | None = False
    subscribers_count: Optional[int] | None = 0
    network_count: Optional[int] | None = 0
    forks: Optional[int]
    open_issues: Optional[int]
    watchers: Optional[int]
    license: Optional["RepoLicenseResponse"]


class RepositoryResponse(RepositoryBase):
    id: int


class Repository(RepositoryBase, IDModel, TSModel):  # , table=True):
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="repositories")
    permission: "RepoPermission" = Relationship(back_populates="repository")
    permission_id: int = Field(foreign_key="repo_permission.id")


class RepoLicenseResponse(SQLModel):
    key: Optional[str] | None = None
    name: Optional[str] | None = None
    url: Optional[str] | None = None
    spdx_id: Optional[str] | None = None
    node_id: Optional[str] | None = None
    html_url: Optional[str] | None = None
