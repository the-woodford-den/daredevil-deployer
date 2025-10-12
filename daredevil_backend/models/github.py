from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from .base import IDModel, TSModel


class AppTokenResponse(SQLModel):
    token: str = Field()
    expires_at: str = Field()


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


class AppPermissionsResponse(SQLModel):
    issues: Optional[str] = Field(default=None)
    checks: Optional[str] = Field(default=None)
    contents: Optional[str] = Field(default=None)
    deployments: Optional[str] = Field(default=None)
    additionalProperties: Optional[str] = Field(default=None)


class AppOwnerBase(SQLModel):
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


class AppOwnerResponse(AppOwnerBase):
    id: int


class AppBase(SQLModel):
    slug: str = Field()
    node_id: str = Field()
    client_id: str = Field()
    name: str = Field()
    description: Optional[str] = Field(default=None)
    external_url: str = Field()
    html_url: str = Field()


class AppResponse(AppBase):
    id: int = Field()
    owner: Optional[AppOwnerResponse] = Field(default=None)
    events: list[Optional[str]] = Field(default_factory=list)
    permissions: Optional[AppPermissionsResponse] = Field(default=None)


class App(AppBase, IDModel, TSModel, table=True):
    __tablename__ = "github_apps"
    github_app_id: int
    token: Optional[str] = Field(default=None)
    expires_at: Optional[str] = Field(default=None)


class InstallationAccountResponse(SQLModel):
    name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)
    login: str
    id: int


class InstallationResponse(SQLModel):
    id: int = Field()
    account: InstallationAccountResponse = Field()
    events: list[str] = Field()
    app_id: int = Field()
    app_slug: str = Field()
    access_tokens_url: str = Field()
    html_url: str = Field()
    repositories_url: str = Field()


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


class RepoLicenseResponse(SQLModel):
    key: Optional[str] | None = None
    name: Optional[str] | None = None
    url: Optional[str] | None = None
    spdx_id: Optional[str] | None = None
    node_id: Optional[str] | None = None
    html_url: Optional[str] | None = None


class RepositoryResponse(RepositoryBase):
    topics: list[Optional[str]]
    owner: Optional[AppOwnerResponse]
    license: Optional[RepoLicenseResponse]
    permissions: Optional[RepoPermissionsBase]
    id: int


# class Repository(RepositoryBase, IDModel, TSModel, table=True):
#     user_id: int = Field(foreign_key="user.id")
#     user: "User" = Relationship(back_populates="repositories")


# class AppPermissionsResponse(SQLModel):
#     actions: Optional[str] = Field(default=None)
#     actions_variables: Optional[str] = Field(default=None)
#     administration: Optional[str] = Field(default=None)
#     attestations: Optional[str] = Field(default=None)
#     checks: Optional[str] = Field(default=None)
#     contents: Optional[str] = Field(default=None)
#     dependabot_secrets: Optional[str] = Field(default=None)
#     deployments: Optional[str] = Field(default=None)
#     discussions: Optional[str] = Field(default=None)
#     emails: Optional[str] = Field(default=None)
#     environments: Optional[str] = Field(default=None)
#     followers: Optional[str] = Field(default=None)
#     issues: Optional[str] = Field(default=None)

# class AppPermissionsResponse(SQLModel):
#     actions: Optional[str] = Field(default=None)
#     actions_variables: Optional[str] = Field(default=None)
#     administration: Optional[str] = Field(default=None)
#     attestations: Optional[str] = Field(default=None)
#     checks: Optional[str] = Field(default=None)
#     contents: Optional[str] = Field(default=None)
#     dependabot_secrets: Optional[str] = Field(default=None)
#     deployments: Optional[str] = Field(default=None)
#     discussions: Optional[str] = Field(default=None)
#     emails: Optional[str] = Field(default=None)
#     environments: Optional[str] = Field(default=None)
#     followers: Optional[str] = Field(default=None)
#     issues: Optional[str] = Field(default=None)
