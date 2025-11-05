from fastapi.security import OAuth2PasswordBearer

user_auth = OAuth2PasswordBearer(tokenUrl="/user/login")
