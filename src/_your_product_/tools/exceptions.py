"""Errors raised by tools. See llm/exceptions.py for why these are per-subsystem."""


class ToolError(Exception):
    """A tool could not complete the action it was asked to perform."""
