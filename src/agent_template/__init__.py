"""agent-template: the layout an agentic Python project starts from.

The version has a single source — the installed distribution metadata — so the
number is never written twice and never drifts between `pyproject.toml` and a
`__version__` literal.
"""

from importlib.metadata import PackageNotFoundError, version

try:  # the package is installed (editable or otherwise)
    __version__ = version("agent-template")
except PackageNotFoundError:  # running from a source tree without an install
    __version__ = "0.0.0+unknown"

__all__ = ["__version__"]
