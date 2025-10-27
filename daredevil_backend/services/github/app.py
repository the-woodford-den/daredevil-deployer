from fastapi import Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from dbs import get_async_session
from models.github import AppRecord, AppRecordResponse


class AppService:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session
        pass

    async def get(self, id: int) -> AppRecord | None:
        query = select(AppRecord).where(AppRecord.github_app_id == id)
        app = (await self.session.execute(query)).one_or_none()
        return app

    async def add(self, app_create: AppRecordResponse) -> AppRecord:
        github_app_id = app_create.id
        new_app_obj = app_create
        del new_app_obj["id"]
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
