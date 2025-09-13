from typing import List, Optional

from sqlmodel import Field, Relationship

from .base import IDModel, TSModel


class User(IDModel, TSModel, table=True):
    repositories: Optional[List["Repository"]] = Relationship(back_populates="user")
    github_id: int = Field(foreign_key="repo_owner.id")
    github: "RepoOwner" = Relationship(back_populates="user")
    repo_permissions: List["RepoPermission"] = Relationship(back_populates="user")
