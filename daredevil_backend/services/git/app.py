from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.git import GitApp, GitAppResponse


class GitAppService:
    """The GitAppService handles database actions for creating, searching,
    updating, and deleting git_apps.
    get() finds user by app_id
    add() creates an app (application made for 1 app)
    update() updates an app
    delete() deletes an app
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> GitApp | None:
        query = select(GitApp).where(GitApp.git_id == id)
        app = (await self.session.execute(query)).scalar_one_or_none()
        return app

    async def add(self, app_create: GitAppResponse) -> GitApp:
        new_app = GitApp(
            **app_create.model_dump(exclude="id"), git_id=app_create.id
        )
        self.session.add(new_app)
        await self.session.commit()
        await self.session.refresh(new_app)
        return new_app

    def update(self, app_update: GitAppResponse) -> GitApp:
        pass

    def delete(self, id: int) -> None:
        pass
