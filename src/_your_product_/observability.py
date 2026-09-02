"""The dashboard: logs, traces, cost and latency — configured in one place.

Without it an agent is a black box: it answered, and why is unrecoverable after
the run. Swap `logging` for OpenTelemetry / Logfire / LangSmith here, nowhere
else. A module, not a package, until a second backend arrives.
"""

import logging

from .config import Settings


def configure(settings: Settings) -> None:
    logging.basicConfig(level=settings.log_level)
