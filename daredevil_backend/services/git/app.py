from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.git import GitApp, GitAppResponse


class GitAppService:
    """The GitAppService handles database actions for git_apps."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, git_id: int) -> GitApp | None:
        query = select(GitApp).where(GitApp.git_id == git_id)
        app = (await self.session.execute(query)).scalar_one_or_none()
        return app

    async def add(self, data: GitAppResponse) -> GitApp:
        new_app = GitApp(**data.model_dump(exclude="id"), git_id=data.id)
        self.session.add(new_app)
        await self.session.commit()
        await self.session.refresh(new_app)
        return new_app

    def update(self, app_update: GitAppResponse) -> GitApp:
        pass

    def delete(self, id: int) -> None:
        pass
