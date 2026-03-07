import logfire

from rich import inspect
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.git import GitApp, GitAppRead, GitAppResponse


class GitAppService:
    """The GitAppService handles database actions for git_apps."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, git_id: int) -> GitAppRead:
        query = select(GitApp).where(GitApp.git_id == git_id)
        app = (await self.session.exec(query)).first()

        if app is None:
            logfire.info(f"No git installation: user: #{git_id}")

        return GitAppRead.model_validate(app, from_attributes=True)

    # Fix TODO
    async def get_by_username(self, username: str) -> GitApp | None:
        query = select(GitApp).where(GitApp.username == username)
        app = (await self.session.exec(query)).first()
        return app

    async def add(self, app_resp: GitAppResponse) -> GitAppRead:
        inspect(app_resp)
        new_app = {"git_id": app_resp["id"], **app_resp}
        new_app.pop("id", None)
        new_app.pop("created_at", None)
        new_app.pop("updated_at", None)
        git_app = GitApp.model_validate(new_app)

        self.session.add(git_app)
        await self.session.commit()
        await self.session.refresh(git_app)

        return GitAppRead.model_validate(git_app, from_attributes=True)

    def update(self, app_update: GitAppResponse) -> GitApp:
        pass

    def delete(self, id: int) -> None:
        pass
