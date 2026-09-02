"""The only module that reads the environment. Everything else takes arguments.

Real projects put pydantic-settings here; this stub uses the standard library so
the template stays dependency-free. Names are documented in .env.example.
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Read once at startup, then passed down."""

    llm_model: str = os.environ.get("LLM_MODEL", "")
    log_level: str = os.environ.get("LOG_LEVEL", "INFO")
