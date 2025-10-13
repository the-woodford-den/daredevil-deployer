import time
from pathlib import Path

import jwt
import logfire
from rich import inspect

from .settings import get_settings


class GithubAppLib:
    """The Github App Library for Configuring Authentication"""

    def __init__(self):
        self.settings = get_settings()

    def create_jwt(self, client_id: str):
        with logfire.span("GithubApp Creating its own JWT..."):
            try:
                pk_path = Path.cwd()
                full_path = pk_path / self.settings.gha_private_key

                with open(full_path, "rb") as key_file:
                    signing_key = key_file.read()

                payload = {
                    "iat": int(time.time()),
                    "exp": int(time.time()) + 600,
                    "iss": client_id,
                }
                encoded_jwt = jwt.encode(
                    payload, signing_key, algorithm="RS256"
                )

                return encoded_jwt

            except Exception as e:
                logfire.error(f"Error Message {e}")
