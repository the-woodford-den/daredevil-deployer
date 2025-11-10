from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.git import Repository, RepositoryResponse


class GitRepoService:
    """The GitRepoService handles database actions for git_repos."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Repository | None:
        query = select(Repository).where(Repository.git_id == id)
        repo = (await self.session.execute(query)).scalar_one_or_none()

        return repo

    async def add(self, repo: RepositoryResponse) -> Repository:
        new_repo = Repository(**repo.model_dump(exclude="id"), git_id=repo.id)
        self.session.add(new_repo)

        await self.session.commit()
        await self.session.refresh(new_repo)
        return new_repo

    def update(self, repo: RepositoryResponse) -> Repository:
        pass

    def delete(self, id: int) -> None:
        pass
