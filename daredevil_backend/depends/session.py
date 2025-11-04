from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from dbs import get_async_session

SessionDepend = Annotated[AsyncSession, Depends(get_async_session)]
