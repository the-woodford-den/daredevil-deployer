from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from dbs import get_async_session

SessionDependency = Annotated[AsyncSession, Depends(get_async_session)]
