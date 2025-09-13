from typing import List, Optional

from sqlalchemy import JSON
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
    site_admin: bool


class RepoOwnerResponse(RepoOwnerBase):
    id: int


class RepositoryBase(SQLModel):
    node_id: str
    name: str
    full_name: str
    owner: JSON
    private: bool
    html_url: str
    description: str
    fork: bool
    url: str
    archive_url: str
    assignees_url: str
    blobs_url: str
    branches_url: str
    collaborators_url: str
    comments_url: str
    commits_url: str
    compare_url: str
    contents_url: str
    contributors_url: str
    deployments_url: str
    downloads_url: str
    events_url: str
    forks_url: str
    git_commits_url: str
    git_refs_url: str
    git_tags_url: str
    git_url: str
    issue_comment_url: str
    issue_events_url: str
    issues_url: str
    keys_url: str
    labels_url: str
    languages_url: str
    merges_url: str
    milestones_url: str
    notifications_url: str
    pulls_url: str
    releases_url: str
    ssh_url: str
    stargazers_url: str
    statuses_url: str
    subscribers_url: str
    subscription_url: str
    tags_url: str
    teams_url: str
    trees_url: str
    clone_url: str
    mirror_url: str
    hooks_url: str
    svn_url: str
    homepage: str
    language: Optional[str]
    forks_count: int
    stargazers_count: int
    watchers_count: int
    size: int
    default_branch: str
    open_issues_count: int
    is_template: bool
    topics: List[str]
    has_issues: bool
    has_projects: bool
    has_wiki: bool
    has_pages: bool
    has_downloads: bool
    archived: bool
    disabled: bool
    visibility: str
    pushed_at: str
    created_at: str
    updated_at: str
    permissions: JSON
    allow_rebase_merge: bool
    template_repository: Optional[str]
    temp_clone_token: str
    allow_squash_merge: bool
    allow_auto_merge: bool
    delete_branch_on_merge: bool
    allow_merge_commit: bool
    subscribers_count: int
    network_count: int
    forks: int
    open_issues: int
    watchers: int


class RepositoryResponse(RepositoryBase):
    id: int


class RepoOwner(RepoOwnerBase, IDModel, TSModel, table=True):
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="github")


class Repository(RepositoryBase, IDModel, TSModel, table=True):
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="repositories")
    permission: "RepoPermission" = Relationship(back_populates="repository")
    permission_id: int = Field(foreign_key="repo_permission.id")


class RepoPermission(IDModel, TSModel, SQLModel, table=True):
    admin: bool
    push: bool
    pull: bool
    repository: Repository = Relationship(back_populates="permission")
    repository_id: int = Field(foreign_key="repository.id")
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="repo_permissions")
