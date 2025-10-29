import debugpy
import logfire
from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient, HTTPStatusError
from rich import inspect, print
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from configs import GithubLibrary
from dbs import get_async_session
from models.git import (CreateGitInstallToken, GitApp, GitAppResponse,
                        GitInstall, GitInstallResponse,
                        GitInstallTokenResponse)
from models.user import User, UserCreate
from services import UserService
from services.git import GitAppService, GitInstallService

api = APIRouter(prefix="/git/app")


@api.get(
    "/search/{slug}",
    response_model=GitAppResponse,
    response_model_exclude_unset=True,
)
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
            response.raise_for_status()
            data = response.json()
            app_service = GitAppService(session=session)

            github_app_obj = GitAppResponse.model_validate(data)
            github_app = await app_service.get(id=github_app_obj.id)
            if github_app is None:
                github_app = await app_service.add(app_create=github_app_obj)
                logfire.info("GitHub App Validated & Stored in DB")
            else:
                logfire.info("GitHub App Exists in DB")

            user_service = UserService(session=session)
            data["owner"]["client_id"] = github_app.client_id
            user_obj = UserCreate.model_validate(data["owner"])
            user = await user_service.get(id=user_obj.id)
            if user is None:
                user = await user_service.add(user_create=user_obj)
                logfire.info("User Validated & Stored in DB")
            else:
                logfire.info("User Exists in DB")

        return github_app_obj

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
    "/access/{client_id}",
    response_model=GitAppResponse,
    response_model_exclude_unset=True,
)
async def authenticated_access_app(
    *, client_id: str, session: AsyncSession = Depends(get_async_session)
):
    """This GET request searches Github Api for the Github App"""
    """ That is Associated with the client_id, pem key ... which creates """
    """the JWT that's required with the Api call. The other /apps/{slug} call"""
    """ does not need a JWT but can only grab public data ..."""

    if client_id is None:
        logfire.error("No Client Id means no JWT")
        raise Exception("No Client Id means no JWT")

    jwt = GithubLibrary().create_jwt(client_id=client_id)
    endpoint = "https://api.github.com/app"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {jwt}",
    }

    try:
        async with AsyncClient() as viper:
            response = await viper.get(url=endpoint, headers=headers)
            data = response.json()
            github_app_obj = GitAppResponse.model_validate(data)

            app_search = select(GitApp).where(
                GitApp.github_app_id == github_app_obj.id
            )
            app_owner_obj = github_app_obj.owner
            user_search = select(User).where(User.git_id == app_owner_obj.id)
            user_record = (await session.execute(user_search)).one_or_none()
            app_record = (await session.execute(app_search)).one_or_none()

            if app_record is None:
                app_id = app_record.id
                app_dict = GitAppResponse.model_dump(github_app_obj)
                app_dict["github_app_id"] = app_id
                del app_dict["id"]
                app_obj = GitApp.model_validate(app_dict)
                session.add(app_obj)
                await session.commit()
                await session.refresh(app_obj)
                logfire.info(f"GitHub App in DB, {app_dict}")
            else:
                logfire.info("GitHub App Exists in DB")

            if user_record is None:
                user_id = app_owner_obj.id
                app_owner_obj = data["owner"]
                app_owner_obj["git_id"] = user_id
                del app_owner_obj["id"]
                user_obj = User.model_validate(app_owner_obj)
                session.add(user_obj)
                await session.commit()
                await session.refresh(user_obj)
                logfire.info(f"GitHub User in DB, {user_obj}")
            else:
                logfire.info("Github User Exists in DB")

            logfire.info(
                f"App Record Response has been returned ...{github_app_obj}"
            )
            return github_app_obj

        response.raise_for_status()
    except HTTPStatusError as e:
        logfire.error(f"HTTP Status Error: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"GitHub API error: {e}",
        )

    except Exception as e:
        logfire.error(f"App Error in get_authenticated_app: {e}:{e}")
        raise Exception(f"App Error in get_authenticated_app: {e}:{e}")


@api.get(
    "/installs/search/{username}",
    response_model=GitInstall,
)
async def search_installations(
    *, username: str, session: AsyncSession = Depends(get_async_session)
):
    """This GET request searches Github Api for Github App GitInstalls."""
    """It searches by username and needs a jwt for authorization."""
    """A Github App client_id is required to create the jwt."""
    """From the list, it compares and pulls from the db by the App slug"""

    user_service = UserService(session)
    user = await user_service.get_by_username(username)
    inspect(user)

    if user is None:
        logfire.error("No User means no JWT")
        raise Exception("No User means no JWT")
    elif user.client_id is None:
        logfire.error("No Client Id means no JWT")
        raise Exception("No Client Id means no JWT")
    logfire.info("Found user with client_id ...")

    github_library = GithubLibrary()
    jwt = github_library.create_jwt(client_id=user.client_id)

    endpoint = "https://api.github.com/app/installations"
    header = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {jwt}",
    }

    with logfire.span("Sending request for app installations list"):
        try:
            async with AsyncClient() as viper:
                response = await viper.get(url=endpoint, headers=header)
                response.raise_for_status()
                i_responses = response.json()

            logfire.info("checking returned list of installations...")
            for i_response in i_responses:
                installation_service = GitInstallService(session)
                inspect(i_response)
                if i_response["account"]["login"] == "woodFordR":
                    install_obj = GitInstallResponse.model_validate(i_response)
                    logfire.info("username matched, checking db record...")
                    installation = await installation_service.get(
                        install_obj.id
                    )
                    inspect(installation)
                    if installation is None:
                        logfire.info(f"Adding GitInstall: {install_obj}")
                        installation = await installation_service.add(
                            install_obj
                        )
                    return installation
                else:
                    return {"status_code": 404, "msg": "No Installation Found"}

        except HTTPStatusError as e:
            logfire.error(f"Internal Error: {e}")
            raise HTTPException(
                status_code=e,
                detail=f"Internal Error: {e}",
            )


@api.post(
    "/install/token",
    response_model=GitInstallTokenResponse,
)
async def installation_token(
    *,
    params: CreateGitInstallToken,
    session: AsyncSession = Depends(get_async_session),
):
    """This post request will provide a response that will include an installation"""
    """access token, the time that the token expires, the permissions that the token has, """
    """and the repositories that the token can access, if applicable. The installation access """
    """ token will expire after 1 hour."""

    inspect(params)

    # # Start debugpy server if not already listening
    # try:
    #     debugpy.listen(("0.0.0.0", 5678))
    #     logfire.info("Debugpy server started on port 5678")
    # except RuntimeError:
    #     pass  # Already listening
    #
    # logfire.info("Waiting for debugger to attach...")
    # debugpy.wait_for_client()  # Pauses here until debugger connects
    # debugpy.breakpoint()

    statement = (
        select(
            GitInstall.app_id,
            GitApp.git_id,
            GitApp.client_id,
        )
        .where(GitInstall.app_id == GitApp.git_id)
        .where(GitInstall.git_id == params.git_id)
    )
    results = (await session.execute(statement)).all()

    if not results:
        logfire.error("No installation found with that install_id")
        raise HTTPException(status_code=404, detail="GitInstall not found")

    client_id = results[-1].client_id
    logfire.info(f"Found GitInstall with client_id: {client_id}")
    github_app_library = GithubLibrary()
    app_jwt = github_app_library.create_jwt(client_id=client_id)

    endpoint = f"https://api.github.com/app/installations/{str(params.git_id)}/access_tokens"
    header = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {app_jwt}",
    }

    with logfire.span("Sending request for installation access token..."):
        try:
            async with AsyncClient() as client:
                response = await client.post(url=endpoint, headers=header)
                response.raise_for_status()
                token_json = response.json()

            logfire.info(f"validating access token ...{token_json}")
            token_obj = GitInstallTokenResponse.model_validate(token_json)

            logfire.info("Responding with token ...")
            return token_obj

        except HTTPStatusError as e:
            logfire.error(f"Internal Error: {e}")
            raise HTTPException(
                status_code=e,
                detail=f"Internal Error: {e}",
            )

    # text(`SELECT app_id from github_installation_records where installation_id = install_id UNION SELECT client_id from github_app_records where github_app_id = app_id`)
    # results = (await session.execute(query_string)).all()

    # results = session.exec(statement)
    # query_alpha = select(GitInstall.app_id).where(
    #     GitInstall.installation_id == install_id
    # )
    # query_omega = select(GitApp.client_id).where(
    #     GitApp.github_app_id == GitInstall.app_id
    # )
    # # union_sigma = query_alpha.union_all(query_omega)


# curl --request POST \
# --url "https://api.github.com/app/installations/INSTALLATION_ID/access_tokens" \
# --header "Accept: application/vnd.github+json" \
# --header "Authorization: Bearer JWT" \
# --header "X-GitHub-Api-Version: 2022-11-28"
#


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
#     app_jwt = GithubLibrary.create_jwt(g_app.client_id)
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
#         logfire.error(f"GHA GitInstall Get Error: {e.status_code}")
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
# gha_lib = GithubLibrary()
# app_jwt = gha_lib.create_jwt(client_id=client_id)
#     "Authorization": f"Bearer {app_jwt}",
# url = f"https://api.github.com/users/{username}/installation"
# u.model_dump_json(exclude=set("password")
# class ApiError(SQLModel):
#     status_code: Literal[401, 403, 404, 422]
