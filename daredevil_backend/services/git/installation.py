import logfire

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.exceptions import HTTPException

from models.git import GitInstallation as Git_I
from models.git import GitInstallationResponse as Git_I_Resp
from models.git import GitInstallationRead as Git_I_Read
from models.git import GitInstallationUpdate as Git_I_Update


class GitInstallationService:
    """The GitInstallationService handles database actions for
    git_installations of a git app."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Git_I_Read:
        statement = select(Git_I).where(Git_I.git_id == id)
        resp = (await self.session.exec(statement)).first()

        if resp is None:
            logfire.info(f"No git installation: user: #{id}")
            raise HTTPException(status_code=404, detail="GitInstall not found")
        return Git_I_Read.model_validate(resp)

    async def get_by_username(self, username: str) -> Git_I_Read | None:
        query = select(Git_I).where(Git_I.login == username)
        install = (await self.session.exec(query)).scalar_one_or_none()
        return install

    async def add(self, ins_resp: Git_I_Resp) -> Git_I_Read:
        merge = {"git_id": ins_resp.model_dump(include={"id"})} | {
            **ins_resp.model_dump(exclude={"id"})
        }
        new_installation = Git_I.model_validate(merge)

        self.session.add(new_installation)
        await self.session.commit()
        await self.session.refresh(new_installation)

        return Git_I_Read.model_validate(new_installation)

    async def update(self, installation: Git_I_Update) -> GitInstallationRead:
        pass

    async def delete(self, id: int) -> None:
        pass
