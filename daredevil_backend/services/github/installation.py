from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.github import InstallationRecord, InstallationRecordResponse


class InstallationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int):
        pass

    async def add(
        self, create_installation: InstallationRecordResponse
    ) -> InstallationRecord:
        pass

    async def update(
        self, update_installation: InstallationRecordResponse
    ) -> InstallationRecord:
        pass

    async def delete(self, id: int) -> None:
        pass
