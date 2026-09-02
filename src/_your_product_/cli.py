"""The terminal entry point: `python -m _your_product_.cli`.

A thin shell — parse, build, call, print. Logic that lives here cannot be
imported or tested by anything else, so keep it to wiring.
"""

import argparse
import sys

from . import __version__


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="_your_product_")
    parser.parse_args(argv)
    print(__version__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
