from typing import TYPE_CHECKING, List, Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from .base import IDModel, TSModel

if TYPE_CHECKING:
    from .user import User


class OAuthAccessTokenResponse(SQLModel):
    access_token: str
    token_type: str
    scope: str


class CreateTokenResponse(SQLModel):
    device_code: str
    user_code: str
    verification_uri: str
    expires_in: int
    interval: int


class UserResponse(SQLModel):
    id: UUID
    device_code: str
    user_code: str
    verification_uri: str
    expires_in: int
    interval: int
    client_id: Optional[str] = None
    access_token: Optional[str] = None


class AppMergeQueuesResponse(SQLModel):
    # metadata: str
    packages: str
    pages: str
    profile: str
    pull_requests: str
    repository_advisories: str
    repository_custom_properties: str
    repository_hooks: str
    repository_projects: str
    secrets: str
    secret_scanning_alerts: str
    secret_scanning_bypass_requests: str
    security_events: str
    starring: str
    statuses: str
    user_events: str
    vulnerability_alerts: str
    watching: str
    workflows: str


class AppPermissionsResponse(SQLModel):
    actions: str
    actions_variables: str
    administration: str
    attestations: str
    checks: str
    contents: str
    dependabot_secrets: str
    deployments: str
    discussions: str
    emails: str
    environments: str
    followers: str
    issues: str


class AppBase(SQLModel):
    client_id: str
    slug: str
    node_id: str
    name: str
    description: str
    external_url: str
    html_url: str
    created_at: str
    updated_at: str
    installations_count: int | None = 0


class AppResponse(AppBase):
    id: int
    events: List[str] = []
    permissions: AppPermissionsResponse
    merge_queues: AppMergeQueuesResponse


class App(AppBase, IDModel, TSModel, table=True):
    github_app_id: int


class AppOwnerBase(SQLModel):
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


class AppOwnerResponse(AppOwnerBase):
    id: int


class AppOwner(AppOwnerBase):
    github_id: int


class RepoPermissionsBase(SQLModel):
    admin: bool
    push: bool
    pull: bool
    maintain: bool
    triage: bool


class RepositoryBase(SQLModel):
    node_id: Optional[str]
    name: Optional[str]
    full_name: Optional[str]
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


class RepositoryResponse(RepositoryBase):
    topics: List[Optional[str]]
    owner: Optional[AppOwnerResponse]
    license: Optional["RepoLicenseResponse"]
    permissions: Optional[RepoPermissionsBase]
    id: int


# class Repository(RepositoryBase, IDModel, TSModel, table=True):
#     user_id: int = Field(foreign_key="user.id")
#     user: "User" = Relationship(back_populates="repositories")


class RepoLicenseResponse(SQLModel):
    key: Optional[str] | None = None
    name: Optional[str] | None = None
    url: Optional[str] | None = None
    spdx_id: Optional[str] | None = None
    node_id: Optional[str] | None = None
    html_url: Optional[str] | None = None
