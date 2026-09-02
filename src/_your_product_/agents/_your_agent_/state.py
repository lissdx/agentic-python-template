"""What the agent carries between steps. Typed, so a wrong key is a build error."""

from typing import TypedDict


class State(TypedDict):
    """LangGraph merges updates into this shape."""

    question: str
    answer: str
