# notebooks/

Two genres, kept apart because they want opposite things from version control.

| Directory | What it is | Outputs |
|---|---|---|
| `experiments/` | exploration: does this chunking work, why did the classifier miss this | **stripped** — gated in CI |
| `tutorials/` | material for someone else to read and run | **kept** — they are what the reader came for |

Naming, from the data-science convention: a number for ordering, initials, and a
short description — `1.0-yl-chunking-window-sweep.ipynb`. The number sorts the
history of an investigation without anyone maintaining an index.

## Why outputs are treated differently

An experiment is run against real inputs, and its outputs carry them: an address,
a fragment of a document, a key printed from the environment. Deleting the cell
later does not remove it from git history. So `experiments/` is checked in CI —
`scripts/check_notebook_outputs.py` fails the build on any committed output. Run
`make notebooks-clean` before committing, or install `nbstripout` once and forget
about it.

A tutorial is the opposite: the reader wants to see what the code prints without
running it, so its outputs are the deliverable. Ragas keeps them in every
notebook under `docs/howtos/`. The rule that comes with that: **a tutorial runs
against synthetic or public data only** — never against anything real.

Phoenix shows the cost of leaving this unstated. Across its `tutorials/`, some
notebooks carry outputs and some do not — `evals_introduction.ipynb` has twelve
cells with output, `evals_quickstart.ipynb` has none — and nothing says which
state was intended.

## What does not belong here

Notebooks generated from source files. That pattern pays off when the notebook is
derived from code someone maintains; for exploration and for teaching, the
notebook *is* the source.
