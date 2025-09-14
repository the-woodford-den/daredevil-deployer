import time
from pathlib import Path

import jwt
import logfire
from rich import inspect

from .settings import get_settings


class GithubJWT:

    def __init__(self):
        settings = get_settings()
        self.gh_username = settings.gh_username
        self.gha_client_id = settings.gha_client_id
        self.gha_pk_path = settings.gha_private_key

    def generate(self):
        with logfire.span("creating auth jwt"):
            try:
                pk_path = Path.cwd()
                full_path = pk_path / self.gha_pk_path

                with open(full_path, "rb") as key_file:
                    signing_key = key_file.read()

                payload = {
                    "iat": int(time.time()),
                    "exp": int(time.time()) + 600,
                    "iss": self.gha_client_id,
                }
                github_jwt = jwt.encode(payload, signing_key, algorithm="RS256")

                return github_jwt

            except Exception as e:
                logfire.error(f"Error Message {e}")
