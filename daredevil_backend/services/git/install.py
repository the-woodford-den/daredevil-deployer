from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.git import GitInstall, GitInstallResponse


class GitInstallService:
    """The GitInstallService handles database actions for creating, searching,
    updating, and deleting git_installs of a git app.
    get() finds user by id
    add() creates an installation (application made for many installations)
    update() updates an installation
    delete() deletes an installation
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> GitInstall | None:
        statement = select(GitInstall).where(GitInstall.git_id == id)
        installation = (
            await self.session.execute(statement)
        ).scalar_one_or_none()
        return installation

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
