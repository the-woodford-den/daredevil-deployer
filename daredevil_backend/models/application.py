from .base import IDModel, TSModel


class ApplicationBase(IDModel, TSModel):
    name: str
    repo: str
