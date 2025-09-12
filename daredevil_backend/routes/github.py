import asyncio
import time

import logfire
from fastapi import APIRouter, HTTPException
from httpx import AsyncClient
from rich import inspect, print

from ..models.github import GithubRepoRead

api = APIRouter(prefix="/github")

logfire.configure(service_name="daredevil")


# OAuth Device Authorization
@api.post("/create-token")
async def create_token(*, client_id: str):
    endpoint = f"https://github.com/login/device/code"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    with logfire.span("requesting github device-flow user token ..."):
        try:
            async with AsyncClient() as viper:
                auth_req_response = await viper.post(
                    url=endpoint, headers=headers, data={"client_id": client_id}
                )

                # device_code, user_code,
                # verification_uri, expires_in, interval
                auth_request = auth_req_response.json()
                if "device_code" in auth_request:
                    device_code = auth_request["device_code"]
                else:
                    raise Exception("no device code!")
                interval = auth_request.get("interval", 5)
                expires_in = auth_request.get("expires_in", 600)

            print(auth_request)
            logfire.info(f"github login info: {auth_request}")
            endpoint = "https://github.com/login/oauth/access_token"
            grant_type = "urn:ietf:params:oauth:grant-type:device_code"

            logfire.info("polling user access token with code ...")
            start_time = time.time()
            async with AsyncClient() as viper:
                while time.time() - start_time < expires_in:
                    auth_device_code_response = await viper.post(
                        url=endpoint,
                        headers=headers,
                        data={
                            "client_id": client_id,
                            "device_code": device_code,
                            "grant_type": grant_type,
                        },
                    )

                    response_data = auth_device_code_response.json()
                    if "access_token" in response_data:
                        user_access_token = response_data["access_token"]
                        logfire.info(
                            f"Github user access token obtained: {user_access_token}"
                        )
                        return user_access_token
                    elif "error" in response_data:
                        error = response_data.get("error")
                        match error:
                            case "authorization_pending":
                                logfire.info("authorization is pending")
                                await asyncio.sleep(interval)
                            case "slow_down":
                                logfire.info("authorization slow down")
                                interval += 5
                                await asyncio.sleep(interval)
                            case _:
                                if error in ["expired_token", "access_denied"]:
                                    logfire.error(f"Github oauth error: {error}")
                                    raise Exception(f"Github oauth failed: {error}")
                    else:
                        logfire.error(
                            f"Unexpected github oauth error in response: {response_data}"
                        )
                        await asyncio.sleep(interval)
                    continue

            logfire.error("GitHub OAuth polling timed out")
            raise Exception("GitHub OAuth polling timed out")

        except Exception as e:
            logfire.error(f"Authentication request failed with : {e}")
            raise Exception(f"Authentication request failed with : {e}")


@api.get("/repos")
async def get_repos(*, user_token: str) -> GithubRepoRead:
    endpoint = f"https://api.github.com/user/repos"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"Bearer {user_token}",
    }

    with logfire.span("... grabbing list of user repositories ..."):
        try:
            async with AsyncClient(timeout=60) as viper:
                response = await viper.get(
                    headers=headers,
                    url=endpoint,
                )
                gh_repo_obj = GithubRepoRead.model_validate(response)

                return gh_repo_obj

        except HTTPException as e:
            logfire.error("Error Message {msg=}", msg=e)
            raise HTTPException(status_code=e.status_code, detail=e.detail)
