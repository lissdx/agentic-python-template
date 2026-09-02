"""What a tool has to look like. Beside the seam it describes, not central."""

from typing import Protocol


class Tool(Protocol):
    name: str

    def run(self, argument: str) -> str: ...
