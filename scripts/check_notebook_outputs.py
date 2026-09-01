"""Fail if a committed experiment notebook carries execution outputs.

An experiment runs against real inputs, so its outputs carry them — an address, a
fragment of a document, a key printed from the environment. git history does not
forget, which makes this the cheapest leak channel in the repository and the one
nobody notices.

Only `notebooks/experiments/` is checked. Tutorials keep their outputs on
purpose: the reader wants to see what the code prints without running it.

    python scripts/check_notebook_outputs.py            # check
    python scripts/check_notebook_outputs.py --fix      # strip, in place
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CHECKED = Path("notebooks/experiments")


def cells_with_output(notebook: dict[str, Any]) -> list[int]:
    """Indices of code cells that carry an output or an execution count."""
    dirty: list[int] = []
    for index, cell in enumerate(notebook.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        if cell.get("outputs") or cell.get("execution_count") is not None:
            dirty.append(index)
    return dirty


def strip(notebook: dict[str, Any]) -> None:
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="strip outputs in place")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)

    root: Path = args.root.resolve()
    target = root / CHECKED
    if not target.is_dir():
        return 0

    failed = False
    for path in sorted(target.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in path.parts:
            continue
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            print(f"{path.relative_to(root)}: not readable as a notebook ({exc})", file=sys.stderr)
            failed = True
            continue

        dirty = cells_with_output(notebook)
        if not dirty:
            continue

        if args.fix:
            strip(notebook)
            path.write_text(
                json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            print(f"stripped {len(dirty)} cell(s) in {path.relative_to(root)}")
        else:
            print(
                f"{path.relative_to(root)}: {len(dirty)} cell(s) carry output "
                f"(cells {', '.join(str(i) for i in dirty)}). Run `make notebooks-clean`.",
                file=sys.stderr,
            )
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
