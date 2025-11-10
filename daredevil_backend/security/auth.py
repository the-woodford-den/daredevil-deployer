from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyCookie, HTTPBearer, OAuth2PasswordBearer

from utility import decode_token

cookie_scheme = APIKeyCookie(name="daredevil_token")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

CookieDepend = Annotated[str, Depends(cookie_scheme)]


class AccessTokenBearer(HTTPBearer):
    async def __call__(self, request):
        auth_credentials = await super().__call__(request)
        token = auth_credentials.credentials
        data = decode_token(token)

        if data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Token, Not Authorized!",
            )

        return data


# token_bearer = AccessTokenBearer()
# Annotated[dict, Depends(token_bearer)]
