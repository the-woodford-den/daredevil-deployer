import logfire
from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient, HTTPStatusError
from rich import inspect
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import GithubAppLib
from dbs import get_async_session
from models import User
from models.github import (AppRecord, AppRecordResponse,
                           InstallationRecordResponse)

api = APIRouter(prefix="/github/app")


@api.get("/search/{slug}", response_model=AppRecordResponse)
async def search_apps(
    *, slug: str, session: AsyncSession = Depends(get_async_session)
):
    """This GET request searches Github Api for a Github App."""
    """It uses a slug to search, only works if you have the App installed on your """
    """github user account. We then check the database and add if it don't exist."""

    url = f"https://api.github.com/apps/{slug}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "daredevil-deployer",
    }

    try:
        async with AsyncClient() as viper:
            response = await viper.get(url=url, headers=headers)
            data = response.json()
            github_app_obj = AppRecordResponse.model_validate(data)

            statement = select(AppRecord).where(
                AppRecord.github_app_id == github_app_obj.id
            )
            inspect(github_app_obj)

            github_app = (await session.execute(statement)).one_or_none()
            if github_app is None:
                gha_id = github_app_obj.id
                app_dict = AppRecordResponse.model_dump(github_app_obj)
                del app_dict["id"]
                app_dict["github_app_id"] = gha_id
                app_obj = AppRecord.model_validate(app_dict)
                session.add(app_obj)
                await session.commit()
                await session.refresh(app_obj)
                logfire.info("GitHub App Validated & Stored in DB")
            else:
                logfire.info("GitHub App Exists in DB")

        return github_app_obj

        response.raise_for_status()
    except HTTPStatusError as e:
        logfire.error(f"HTTP Status Error: {e}")

        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"GitHub API error: {e}",
        )
    except Exception as e:
        logfire.error(f"App Error in search_apps: {e}:{e}")
        raise Exception(f"App Error in search_apps: {e}:{e}")


@api.get(
    "/installation/search/{username}", response_model=InstallationRecordResponse
)
async def search_installations(
    *, username: str, async_session: AsyncSession = Depends(get_async_session)
):
    """This GET request searches Github Api for Github App Installations."""
    """It searches by username and needs a jwt for authorization."""
    """A Github App client_id is required to create the jwt."""
    """From the list, it compares and pulls from the db by the App slug"""

    statement = select(AppRecord).where(AppRecord.slug == "daredevil-deployer")
    github_app = (await async_session.exec(statement)).first()

    gha_lib = GithubAppLib()
    app_jwt = gha_lib.create_jwt(client_id=github_app.client_id)

    endpoint = "https://api.github.com/app/installations"
    header = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {app_jwt}",
    }

    with logfire.span("Sending request for app installations list"):
        try:
            async with AsyncClient() as client:
                response = await client.get(url=endpoint, headers=header)
                logfire.info(f"installations list response: {response.json()}")

                response.raise_for_status()
                install_responses = response.json()

            for app_install in install_responses:
                if app_install["account"]["login"] == username:
                    install_obj = InstallationRecordResponse.model_validate(
                        app_install
                    )
                    return install_obj

            response.raise_for_status()
        except HTTPStatusError as e:
            logfire.error(f"HTTP Status Error: {e.response.status_code}")

            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"GitHub API error: {e.response.text}",
            )


@api.get("/user/{client_id}")
async def search_apps_users(
    *, client_id: str, async_session: AsyncSession = Depends(get_async_session)
):
    """With the App's client_id, this route returns its data."""
    """Then, we check the database to see if the App or User / Owner """
    """exist. We then add / do nothing, then return the data."""
    """This route requires a jwt."""

    jwt = GithubAppLib.create_jwt(client_id)

    endpoint = "https://api.github.com/app"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {jwt}",
    }

    with logfire.span("asking github api for user access..."):
        try:
            async with AsyncClient() as viper:
                response = await viper.get(url=endpoint, headers=headers)
                auth_response = response.json()

            statement = select(User).where(
                User.github_id == auth_response["owner"]["id"]
            )
            user = (await async_session.exec(statement)).one_or_none()
            if user is None:
                github_id_value = auth_response["owner"]["id"]
                auth_response["owner"]["github_id"] = github_id_value
                del auth_response["owner"]["id"]
                create_user = auth_response["owner"]
                user_obj = User.model_validate(create_user)
                async_session.add(user_obj)
                await async_session.commit()
                await async_session.refresh(user_obj)
                user = user_obj
                logfire.info(f"User {user_obj} created!")

            del auth_response["owner"]
            statement = select(AppRecord).where(
                AppRecord.github_app_id == auth_response["id"]
            )
            github_app = (await async_session.exec(statement)).one_or_none()
            if github_app is None:
                app_id_value = auth_response["id"]
                del auth_response["id"]
                auth_response["github_app_id"] = app_id_value
                create_github_app = auth_response
                app_obj = AppRecord.model_validate(create_github_app)
                async_session.add(app_obj)
                await async_session.commit()
                await async_session.refresh(app_obj)
                logfire.info(f"Github App {app_obj.slug} created!")

            return auth_response
        except Exception as e:
            logfire.error("error message: {msg=}", msg=e)


# # Get the Authenticated GitHub App
# @api.post("/get-auth-app")
# async def get_auth_app(*, client_id: str) -> AppTokenResponse:
#     session = await get_async_session()
#     async with session:
#         statement = select(App).where(App.github_app_id == gha_id)
#         g_app = (await session.exec(statement)).one_or_none()
#         if g_app is None:
#             return {"status_code": 404, "message": "Not Found."}
#
#     app_jwt = GithubAppLib.create_jwt(g_app.client_id)
#
#     url = f"https://api.github.com/app/installations/{g_app.github_app_id}/access_tokens"
#     headers = {
#         "Accept": "application/vnd.github+json",
#         "X-GitHub-Api-Version": "2022-11-28",
#         "Authorization": f"Bearer {app_jwt}",
#         "User-Agent": "daredevil-deployer",
#     }
#
#     try:
#         async with AsyncClient() as viper:
#             response = await viper.post(url=url, headers=headers)
#             inspect(response.json())
#             gh_app_token_obj = AppTokenResponse.model_validate(response.json())
#             inspect(gh_app_token_obj)
#
#         return gh_app_token_obj
#     except Exception as e:
#         logfire.error(f"GHA Installation Get Error: {e.status_code}")
#         raise Exception(f"Error: {e.status_code}")
#
#
# @api.websocket("/poll-create-token/{id}")
# async def poll_create_token(*, id: str, websocket: WebSocket):
#     await manager.connect(websocket)
#     session = await get_async_session()
#     async with session:
#         statement = select(User).where(User.id == id)
#         user = (await session.exec(statement)).one_or_none()
#         inspect(user)
#     interval = user.interval or 15
#     logfire.info(f"Starting polling with interval: {interval} seconds")
#
#     while True:
#         token_link = "https://github.com/login/oauth/access_token"
#         header = {
#             "Accept": "application/vnd.github+json",
#             "X-GitHub-Api-Version": "2022-11-28",
#             "User-Agent": "daredevil-token-depot",
#         }
#         grant_type = "urn:ietf:params:oauth:grant-type:device_code"
#
#         logfire.info("polling user access token with code ...")
#         await manager.send_update(
#             f"polling user access token at github (waiting {interval}s) ...",
#             websocket,
#         )
#         start_time = time.time()
#         try:
#             while time.time() - start_time < user.expires_in:
#                 # Wait for the interval before polling
#                 logfire.info(f"Waiting {interval}s before next poll...")
#                 await asyncio.sleep(interval)
#
#                 async with AsyncClient() as viper:
#                     response = await viper.post(
#                         url=token_link,
#                         headers=header,
#                         data={
#                             "client_id": user.client_id,
#                             "device_code": user.device_code,
#                             "grant_type": grant_type,
#                         },
#                     )
#
#                     oauth_response = response.json()
#                     logfire.info(f"GitHub response: {oauth_response}")
#
#                     if "access_token" in oauth_response:
#                         oa_atr_model = OAuthAccessTokenResponse.model_validate(
#                             oauth_response
#                         )
#                         logfire.info("GH user access token collected")
#                         await manager.send_update(
#                             f"OAuth token retrieved: {oa_atr_model.access_token}",
#                             websocket,
#                         )
#                         async with session:
#                             user.access_token = oa_atr_model.access_token
#                             session.add(user)
#                             await session.commit()
#                             await session.refresh(user)
#                             print(user)
#
#                         manager.disconnect(websocket)
#                         inspect(user)
#                         break
#                     elif "error" in oauth_response:
#                         error = oauth_response.get("error")
#                         match error:
#                             case "authorization_pending":
#                                 logfire.info("Authorization is Pending")
#                                 await manager.send_update(
#                                     "Authorization is Pending", websocket
#                                 )
#                             case "slow_down":
#                                 interval += 10
#                                 logfire.info(
#                                     f"authorization slow down - increasing interval to {interval}s"
#                                 )
#                                 await manager.send_update(
#                                     f"Authorization Slow Down - waiting {interval}s",
#                                     websocket,
#                                 )
#                             case "incorrect_device_code":
#                                 logfire.info(
#                                     "Incorrect Device Code, Try Again."
#                                 )
#                                 await manager.send_update(
#                                     "Incorrect Device Code, Try Again.",
#                                     websocket,
#                                 )
#                             case _:
#                                 if error in [
#                                     "expired_token",
#                                     "access_denied",
#                                     "device_flow_disabled",
#                                     "unsupported_grant_type",
#                                     "incorrect_client_credentials",
#                                 ]:
#                                     raise Exception(error)
#                         continue
#
#         except Exception as e:
#             logfire.error(f"GitHub OAuth Polling Error: {e.msg}")
#             await manager.send_update(
#                 f"GitHub OAuth Polling Error: {e.msg}", websocket
#             )
#             manager.disconnect(websocket)
#             raise Exception(f"Error: {e.msg}")
#         finally:
#             logfire.info("GitHub OAuth polling closed")
#             await manager.send_update("GitHub OAuth polling closed.", websocket)
#             manager.disconnect(websocket)
# gha_lib = GithubAppLib()
# app_jwt = gha_lib.create_jwt(client_id=client_id)
#     "Authorization": f"Bearer {app_jwt}",
# url = f"https://api.github.com/users/{username}/installation"
# u.model_dump_json(exclude=set("password")
# class ApiError(SQLModel):
#     status_code: Literal[401, 403, 404, 422]
