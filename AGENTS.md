# agent-template — instructions for coding agents

Vendor-neutral by design: `CLAUDE.md` is a symlink to this file, so every tool
reads one source and no vendor's filename becomes the carrier. Repository
purpose: see [README.md](README.md).

## Layout

The rule behind the whole table: **what is needed at runtime lives inside the
package; what is needed only by a developer lives outside it.** Only
`src/agent_template` is listed in `[tool.hatch.build.targets.wheel]`, so a
top-level directory is not importable from an installed distribution — the
boundary is enforced by the build, not by convention.

| Path | Holds | Ships in the wheel |
|---|---|---|
| `src/agent_template/contracts/` | pydantic models — the shared vocabulary | yes |
| `src/agent_template/agents/` | one file per agent: the thing that decides | yes |
| `src/agent_template/tools/` | one file per tool: the thing that acts | yes |
| `src/agent_template/prompts/` | prompt text, loaded at runtime | yes |
| `src/agent_template/model/` | the single seam to the LLM provider | yes |
| `src/agent_template/obs/` | logging, tracing, metrics, cost | yes |
| `src/agent_template/config/` | settings, read once and validated | yes |
| `src/agent_template/cli/` | command-line entry points | yes |
| `src/agent_template/evaluators/` | the graders — how an output is scored | yes |
| `src/agent_template/evals/` | the runs — datasets and the entry point CI calls | yes |
| `src/agent_template/exceptions.py` | the error taxonomy, one root | yes |
| `tests/unit/`, `tests/integration/` | tests | no |
| `db/migrations/` | schema history, executed by a migration tool | no |
| `docs/`, `examples/`, `scripts/`, `deploy/` | developer-facing material | no |
| `.github/workflows/` | CI | no |

Two boundaries inside the package are deliberate:

- **`agents/` decides, `tools/` acts.** An agent chooses; a tool performs. They
  change for different reasons — a new capability is a tool, a new judgement is
  an agent — so they do not share a file.
- **`evaluators/` grade, `evals/` run.** An evaluator is a library: given an
  output and a gold label, it produces a score. An eval is an entry point: it
  loads a dataset, drives the system, applies the evaluators and reports. CI
  calls the second and never the first. Collapsing them is the same mistake as
  putting a test inside the code it tests.

**Create a subpackage when the subsystem exists, not before.** The tree is read
as an architecture diagram; an empty `memory/` or `hitl/` describes a system that
was never built. Add them — and `safety/`, `persistence/`, `gen/` — the day there
is something to put in them, and give each one a docstring that says what belongs
there and what does not.

## Conventions

- **English only** — code, comments, docs, README, commit messages. No exceptions.
- **`uv` owns the environment.** Never `pip install` into `.venv`, never create it
  with `virtualenv`. `uv sync` after pulling; `uv add <pkg>` to add a dependency.
  `uv.lock` is committed and never hand-edited.
- **`pyproject.toml` is the only home for tool configuration.** No `setup.cfg`, no
  `.flake8`, no `mypy.ini`.
- **Tooling that only the repository needs goes in `[dependency-groups]`** (PEP
  735), never in `[project.optional-dependencies]` — the latter ships to whoever
  installs the package.
- **The version has one source**: the installed distribution metadata, read in
  `src/agent_template/__init__.py`. Never a second literal.
- **No absolute paths anywhere in the repository.**

## Commands

`make help` lists them. The ones that matter:

```
make install     # sync the environment from uv.lock
make check       # lint + typecheck + test, in the order CI runs them
```

## What CI gates

`ruff check` → `ruff format --check` → `mypy --strict` → `pytest tests/unit`.
All four block a merge. `uv sync --locked` fails the build when `uv.lock` is
stale, so a dependency added without relocking cannot reach `main`.

A check that nothing triggers is documentation, not a gate: anything worth
enforcing goes into the workflow, not into this file as a request.
