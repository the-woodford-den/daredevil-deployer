from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.git import (
    GitInstallation,
    GitInstallationResponse,
    GitInstallationRead,
    GitInstallationUpdate,
)


class GitInstallationService:
    """The GitInstallationService handles database actions for
    git_installations of a git app."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> GitInstallationRead | None:
        statement = select(GitInstallation).where(GitInstallation.git_id == id)
        installation = (await self.session.exec(statement)).scalar_one_or_none()
        return installation

    async def get_by_username(
        self, username: str
    ) -> GitInstallationRead | None:
        query = select(GitInstallation).where(
            GitInstallation.login == username)
        install = (await self.session.exec(query)).scalar_one_or_none()
        return install

    async def add(
        self, ins_resp: GitInstallationResponse
    ) -> GitInstallationRead:
        merge = {"git_id": ins_resp.model_dump(include={"id"})} | {
            **ins_resp.model_dump(exclude={"id"})
        }
        new_installation = GitInstallation.model_validate(merge)
        self.session.add(new_installation)
        await self.session.commit()
        await self.session.refresh(new_installation)
        return GitInstallationRead.model_validate(new_installation)

    async def update(
        self, installation: GitInstallationUpdate
    ) -> GitInstallationRead:
        pass

    async def delete(self, id: int) -> None:
        pass
