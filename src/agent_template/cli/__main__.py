"""Entry point: `python -m agent_template.cli`.

Deliberately trivial. Its job is to give the container image something to run, so
that "the image works" is a command that exits zero rather than an assumption.
"""

import sys

from agent_template import __version__


def main(argv: list[str] | None = None) -> int:
    del argv  # nothing to parse yet
    print(f"agent-template {__version__}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
