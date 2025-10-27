from rich import inspect
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.github import AppRecord, AppRecordResponse


class AppService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> AppRecord | None:
        query = select(AppRecord).where(AppRecord.github_app_id == id)
        app = (await self.session.execute(query)).one_or_none()
        return app

    async def add(self, app_create: AppRecordResponse) -> AppRecord:
        github_app_id = app_create.id
        new_app_obj = app_create.model_dump(exclude="id")
        new_app_obj["github_app_id"] = github_app_id
        app = AppRecord.model_validate(new_app_obj)
        self.session.add(app)
        await self.session.commit()
        await self.session.refresh(app)
        return app

    def update(self, app_update: AppRecordResponse) -> AppRecord:
        pass

    def delete(self, id: int) -> None:
        pass
