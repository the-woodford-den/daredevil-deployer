import time
from pathlib import Path

import jwt
import logfire

from ..main import get_settings


class GithubJWT:

    def __init__(self):
        with logfire.span("creating auth jwt"):
            try:
                settings = get_settings.cache_info
                self.gh_username = settings.gh_username  # ignore
                # self.gha_client_id = settings.gha_client_id

                payload = {
                    "iat": int(time.time()),
                    "exp": int(time.time()) + 600,
                }
                self.gha_jwt = jwt.encode(payload, self.gh_username, algorithm="RS256")

            except Exception as e:
                logfire.error("Error Message {msg=}", msg=e)

    def __getstate__(self, *args, **kwargs):
        state = self.__dict__
        return state

    def __setstate__(self, state):
        with logfire.span("setting state for user jwt session"):
            for item in state:
                logfire.info("setting item {item=} to {x=}", item=item, x=state[item])
                setattr(self, item, state[item])
