import logfire
from fastapi import APIRouter
from httpx import AsyncClient
from rich import inspect, print

api = APIRouter(prefix="/user")

logfire.configure(service_name="daredevil")


# Step 1 OAuth 2.0 Device Authorization Grant
@api.post("/github/token/code")
async def create_token_code(*, client_id: str):
    endpoint = f"https://github.com/login/device/code"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    with logfire.span("requesting github device-flow user token ..."):
        try:
            async with AsyncClient() as viper:
                response = await viper.post(
                    url=endpoint, headers=headers, data={"client_id": client_id}
                )

            print(response)
            return response.json()
        except Exception as e:
            logfire.error("error message: {msg=}", msg=e)
    # device_code, user_code, verification_uri, expires_in, interval

    # next hit https://github.com/login/device, with user_code.


# with repository_id, client_id, device_code, grant_type = "urn:ietf:params:oauth:grant-type:device_code"
# Step 4 OAuth 2.0 Device Authorization Grant
# Need to Poll with Httpx
@api.post("/github/token/login")
async def create_app_token(*, client_id: str, device_code: str):
    endpoint = f"https://github.com/login/device/code"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    grant_type = "urn:ietf:params:oauth:grant-type:device_code"

    with logfire.span("requesting user access token with code ..."):
        try:
            async with AsyncClient() as viper:
                response = await viper.post(
                    url=endpoint,
                    headers=headers,
                    data={
                        "client_id": client_id,
                        "device_code": device_code,
                        "grant_type": grant_type,
                    },
                )

            print(response)
            return response.json()
        except Exception as e:
            logfire.error("error message: {msg=}", msg=e)
        # access_token, expires_in, refresh_token, refresh_token_expires_in,
        # scope, token_type


# Example API request with user access token
@api.get("/github/user")
async def get_github_user(*, access_token: str):
    endpoint = f"https://api.github.com/user"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {access_token}",
    }

    with logfire.span("accessing github api for user with token ..."):
        try:
            async with AsyncClient() as viper:
                response = await viper.post(url=endpoint, headers=headers)

            print(response)
            return response.json()
        except Exception as e:
            logfire.error("error message: {msg=}", msg=e)
