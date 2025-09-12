import time
from pathlib import Path

import jwt
import logfire

from ..main import get_settings

logfire.configure(service_name="Github-JWT")


class GithubJWT:

    def __init__(self):
        with logfire.span("creating auth jwt"):
            try:
                settings = get_settings()
                self.gh_username = settings.gh_username
                self.gha_client_id = settings.gha_client_id

                if settings.gha_pk_name is not None:
                    gha_pk_file = settings.gha_pk_name + ".pem"
                    self.gha_pk_path = Path(Path.cwd(), gha_pk_file)
                else:
                    self.gha_pk_path = Path(
                        Path.cwd(), "daredevil-backend-private-key.pem"
                    )

                payload = {
                    "iat": int(time.time()),
                    "exp": int(time.time()) + 600,
                    "iss": self.gha_client_id,
                }
                with open(self.gha_pk_path, "rb") as key_file:
                    gha_pk = key_file.read()

                self.gha_jwt = jwt.encode(payload, gha_pk, algorithm="RS256")

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
