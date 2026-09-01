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
| ○ `src/agent_template/memory/` | what the agent remembers | yes |
| ○ `src/agent_template/persistence/` | what outlives the process | yes |
| ○ `src/agent_template/safety/` | guardrails that run *during* a request | yes |
| ○ `src/agent_template/hitl/` | approval, escalation, resume | yes |
| ○ `src/agent_template/gen/` | output of code generators | yes |
| `tests/unit/`, `tests/integration/` | tests | no |
| `notebooks/` | exploration and teaching material | no |
| `docker/` | the image this repository builds | no |
| `devenv/` | the local development environment; ships nothing | no |
| `db/migrations/` | schema history, executed by a migration tool | no |
| `docs/`, `examples/`, `scripts/`, `deploy/` | developer-facing material | no |
| `.github/workflows/` | CI | no |

**○ marks the menu.** Those five subpackages are shipped so the layout decision
is visible without cloning, and each one's docstring opens with `Optional.` — the
marker `make rename DROP_OPTIONAL=1` reads to delete them. **Delete what this
system does not have.** The tree is read as an architecture diagram, and an empty
`hitl/` in a project that never asks a human describes something that was never
built.

Two boundaries inside the package are deliberate:

- **`agents/` decides, `tools/` acts.** An agent chooses; a tool performs. They
  change for different reasons — a new capability is a tool, a new judgement is
  an agent — so they do not share a file.
- **`evaluators/` grade, `evals/` run.** An evaluator is a library: given an
  output and a gold label, it produces a score. An eval is an entry point: it
  loads a dataset, drives the system, applies the evaluators and reports. CI
  calls the second and never the first. Collapsing them is the same mistake as
  putting a test inside the code it tests.

## Containers and the local environment

Nothing about containers appears at the repository root. The two halves split on
the same rule the package follows one level down — **what ships versus what only
a developer needs.** See [docker/README.md](docker/README.md) and
[devenv/README.md](devenv/README.md).

| Path | What it is |
|---|---|
| `docker/Dockerfile` | the image this repository builds |
| `docker/Dockerfile.dockerignore` | its build context — BuildKit reads it from beside the Dockerfile |
| `devenv/docker/compose.yaml` | the local stack |
| `devenv/docker/compose.override.yaml` | development only: exposed ports, bind mounts, debug logging |
| `devenv/docker/postgres/init.sql` | runs once, on an empty data directory |

Docker is one mechanism inside `devenv/`, not its organising idea: seed data,
fixtures, a local cluster and a `direnv` file are development environment too and
are not containers. Grafana arranges it the same way, in `devenv/docker/blocks/`.

Two consequences, both absorbed by the `Makefile` — **never invoke `docker` or
`docker compose` here by hand:**

- the build needs `-f docker/Dockerfile`, since `docker build .` looks at the
  root;
- Compose resolves relative paths and reads `.env` from its project directory,
  which defaults to the first `-f` file's directory — so `make up` passes
  `--project-directory .` and every path inside `compose.yaml` is written from
  the repository root.

Growth: a second image becomes `docker/<name>/Dockerfile`; a second stack becomes
`devenv/docker/<name>/`.

## Notebooks

`notebooks/experiments/` and `notebooks/tutorials/` are two genres with opposite
policies, and mixing them is what turns the directory into a junk drawer.

- **`experiments/` — outputs are stripped, and CI enforces it.** Exploration runs
  against real inputs, and an output carries them into a history that does not
  forget. `make notebooks-clean` before committing.
- **`tutorials/` — outputs are kept, and the data is synthetic.** A reader wants
  to see what the code prints without running it. Nothing real goes in.

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
- **Secrets appear in `.env.example` by name and never by value.**
- **No absolute paths anywhere in the repository.**

## Commands

`make help` lists them. The ones that matter:

```
make install     # sync the environment from uv.lock
make check       # lint + format + typecheck + test + notebooks, in CI order
make up          # start the local stack; make down to stop it
make image       # build the container image and prove it runs
                 # never call docker/docker compose by hand — paths live in the Makefile
```

## What CI gates

`ruff check` → `ruff format --check` → `mypy --strict` → `pytest tests/unit` →
the notebook-output check. All five block a merge, and `uv sync --locked` fails
the build when `uv.lock` is stale, so a dependency added without relocking cannot
reach `main`. A second job builds the image and runs it.

A check that nothing triggers is documentation, not a gate: anything worth
enforcing goes into the workflow, not into this file as a request.
