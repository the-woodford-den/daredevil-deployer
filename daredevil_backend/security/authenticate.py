from fastapi.security import APIKeyCookie

daredevil_user_cookie = APIKeyCookie(name="daredevil_token")
