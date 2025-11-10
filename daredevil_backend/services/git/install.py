from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.git import GitInstall, GitInstallResponse


class GitInstallService:
    """The GitInstallService handles database actions for git_installs of
    a git app.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> GitInstall | None:
        statement = select(GitInstall).where(GitInstall.git_id == id)
        installation = (
            await self.session.execute(statement)
        ).scalar_one_or_none()
        return installation

    async def get_by_username(self, username: str) -> GitInstall | None:
        query = select(GitInstall).where(GitInstall.login == username)
        install = (await self.session.execute(query)).scalar_one_or_none()
        return install

    async def add(self, installation: GitInstallResponse) -> GitInstall:
        new_installation = GitInstall(
            **installation.model_dump(exclude="id"),
            git_id=installation.id,
        )
        self.session.add(new_installation)
        await self.session.commit()
        await self.session.refresh(new_installation)
        return new_installation

    async def update(
        self, update_installation: GitInstallResponse
    ) -> GitInstall:
        pass

    async def delete(self, id: int) -> None:
        pass
