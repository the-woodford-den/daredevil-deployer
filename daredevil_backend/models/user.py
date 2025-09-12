from authlib.jose import JsonWebToken

from .base import IDModel, TSModel


class User(IDModel, TSModel):
    gh_username: str | None
    gha_client_id: str | None
    gha_jwt: JsonWebToken | None

    def __repr__(self):
        return f"<User github-user={self.gh_username}>"
