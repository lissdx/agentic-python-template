"""The contract every provider implements. Lives beside the seam, not in a
central `contracts/` package — that directory appears in one repo of forty.
"""

from typing import Protocol


class Chat(Protocol):
    """The one call the rest of the package is allowed to make."""

    def complete(self, prompt: str) -> str: ...
