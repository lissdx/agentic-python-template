"""The things that act — one file per tool. This module is the registry: the
single place a tool becomes visible to an agent.

A tool performs (reads a mailbox, writes a row, calls an API). It does not decide
whether it should run — that is the agent's job.
"""

from .interface import Tool

TOOLS: list[Tool] = []
