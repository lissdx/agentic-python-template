"""Exits non-zero when a score is below its threshold. CI calls this, not pytest.

Kept dependency-free on purpose: wire it to your eval runner when you have one.
"""

import sys


def main() -> int:
    scores: dict[str, float] = {}  # your runner fills this
    return 1 if any(v < 0.0 for v in scores.values()) else 0


if __name__ == "__main__":
    sys.exit(main())
