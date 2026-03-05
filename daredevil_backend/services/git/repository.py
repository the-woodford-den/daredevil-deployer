from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from models.git import GitRepository, GitRepositoryRead, GitRepositoryResponse


class GitRepositoryService:
    """The GitRepositoryService handles database actions for git_repositories."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> GitRepositoryRead | None:
        query = select(GitRepository).where(GitRepository.git_id == id)
        repo = (await self.session.execute(query)).scalar_one_or_none()

        return repo

    async def add(self, repo: GitRepositoryResponse) -> GitRepositoryRead:
        new_repo = GitRepository(
            **repo.model_dump(exclude="id"), git_id=repo.id
        )
        self.session.add(new_repo)

        await self.session.commit()
        await self.session.refresh(new_repo)
        return new_repo

    def update(self, repo: GitRepositoryResponse) -> GitRepositoryRead:
        pass

    def delete(self, id: int) -> None:
        pass
