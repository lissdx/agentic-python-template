"""The package. Rename this directory to your product; nothing else changes.

The version has one source — installed distribution metadata — so the number is
never written twice.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("your-product")
except PackageNotFoundError:  # a source tree with no install
    __version__ = "0.0.0+unknown"

__all__ = ["__version__"]
