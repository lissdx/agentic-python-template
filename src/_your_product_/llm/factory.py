"""Name to client. The single place where a model is chosen."""

from .base import Chat


def build(model: str) -> Chat:
    # from ._your_provider_ import YourProvider
    # return YourProvider(model=model)
    raise NotImplementedError(model)
