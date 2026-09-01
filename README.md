# agentic-python-template

A starting layout for an agentic Python project — the directory structure, the
tooling and the CI gate, with the reason for each decision written next to it.

**Use this template** → then:

```bash
make rename NAME=my-project    # renames the package everywhere, refreshes the lock
                               # add DROP_OPTIONAL=1 to keep only the core
make install
make check                     # lint → format → types → tests → notebooks, in CI order
make up                        # the local stack: Postgres with pgvector
make image                     # build the container image and run it
```

That is the whole setup. `make check` is green on a fresh clone before you have
written a line, which is the point: the gate exists before the code, rather than
being added once it is already inconvenient.

---

## Where this came from

Thirteen production Python repositories were read against the same grid of
thirty-eight surfaces — how each one declares dependencies, where it keeps
schemas, whether the type-checker actually fails the build, where prompts live,
how tests are split. The specimens included `pydantic/pydantic-ai`,
`openai/openai-agents-python`, `browser-use/browser-use`, `langgenius/dify`,
`PrefectHQ/prefect`, `hynek/svcs` and `fastapi/full-stack-fastapi-template`.

The point of counting rather than asking was to separate what everyone does from
what everyone *says*. Three results were not what the guides claim:

| Claim you usually hear | What the count showed |
|---|---|
| "Use `src/` layout" | **8 of 13.** Libraries yes; large service applications often not. |
| "Get your coverage gate up" | **6 of 13** — a minority practice. |
| — | **13 of 13** make the **type-checker fail the build.** That is the real consensus. |
| "Write ADRs" | **0 of 13** have a formal ADR directory. Architecture gets documented — just never in a file named that. |

Nine surfaces were present in all thirteen, and they are what this template is
built around: a declared package manager, a linter/formatter, a type-checker,
**the type-checker gating CI**, an organised test layout, CI at all, a single
source for the version, a defined home for schemas, and **one seam that owns the
conversation with the model provider**.

## The one rule the layout follows

**What is needed at runtime lives inside the package. What is needed only by a
developer lives outside it.**

This is mechanical, not aesthetic. `pyproject.toml` declares what goes into the
wheel:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/agent_template"]
```

A directory at the repository root is not in that wheel, so an installed
distribution cannot import it. That single fact decides every argument:

| Directory | Where | Because |
|---|---|---|
| `evals/` | **inside** the package | the harness is imported and run against the live system |
| `prompts/` | **inside** | loaded at runtime; a prompt the wheel cannot find is unusable |
| `model/` | **inside** | it *is* the runtime path to the provider |
| `tests/` | **outside** | never shipped |
| `db/migrations/` | **outside** | executed by a migration tool, not by Python |
| `docs/`, `examples/`, `scripts/`, `deploy/` | **outside** | not part of the running product |

Engineers arriving from Go tend to put `gen/` at the repository root, where the
module resolves by path. In Python that directory is simply not importable from
an install. Same instinct, different build model.

## What is in the package, and why

Each directory ships with a docstring stating what belongs there and what does
not — open the `__init__.py` rather than guessing from the name.

| Directory | Holds |
|---|---|
| `contracts/` | pydantic models: the vocabulary every other subpackage speaks |
| `agents/` | the things that **decide** — one file per agent |
| `tools/` | the things that **act** — one file per tool |
| `prompts/` | prompt text, loaded at runtime; long ones as `.md`, one-liners as constants |
| `model/` | the single seam to the provider — nothing else imports an SDK |
| `obs/` | logging, tracing, metrics, cost |
| `config/` | settings, read once and validated at startup |
| `cli/` | entry points; wiring only |
| `evaluators/` | the **graders**: output + gold label → score |
| `evals/` | the **runs**: dataset, drive the system, apply evaluators, report |
| `exceptions.py` | the error taxonomy, one root class |
| ○ `memory/` | what the agent remembers across turns and runs |
| ○ `persistence/` | what outlives the process: checkpoints, repositories |
| ○ `safety/` | guardrails that run **during** a request and can stop it |
| ○ `hitl/` | approval, escalation, and the resume path afterwards |
| ○ `gen/` | output of code generators; committed, never hand-edited |

**○ is the menu, not the minimum.** Those five ship so the decision is visible in
the GitHub tree without cloning, and each one's docstring opens with the word
`Optional.` — which is also the marker `make rename DROP_OPTIONAL=1` reads to
delete them. Keeping one you do not use makes the tree lie about your
architecture, so delete it; the flag does it for you at generation time.

Two boundaries there are worth stating out loud, because both are routinely
collapsed:

- **`agents/` decides, `tools/` acts.** A new capability is a tool; a new
  judgement is an agent. They change on different clocks.
- **`evaluators/` grade, `evals/` run.** CI calls the second and never the first.
  Putting them in one place is the same mistake as putting a test inside the code
  it tests — and indeed both surveyed repositories that have evals also have
  `tests/test_evals.py`, testing the eval code.

`tests/` and `evals/` are different populations, not a hierarchy: `tests/` asks
*does this code do what it was written to do*, `evals/` asks *does the system
still judge the way we judged*. The first is deterministic; the second is not.

## Containers, and where they live

Nothing about containers sits at the repository root, and the two halves split on
the same rule the package follows one level down — **what ships versus what only
a developer needs:**

```
docker/                           what gets built and shipped
├── Dockerfile                    CI builds it and runs it
└── Dockerfile.dockerignore       BuildKit reads it from beside the Dockerfile

devenv/                           what only ever runs on your machine
└── docker/
    ├── compose.yaml              the local stack: Postgres with pgvector
    ├── compose.override.yaml     dev only: exposed port, bind mount, debug logs
    └── postgres/init.sql         runs once, on an empty data directory
```

Docker sits *inside* `devenv/` rather than the other way round, because a
development environment is also seed data, fixtures, a local cluster and a
`direnv` file — none of them containers. Grafana arranges it identically, in
`devenv/docker/blocks/`.

**This is a deliberate departure from the majority, so here is the count and the
cost.** Across forty-seven repositories, **24 keep the shipping `Dockerfile` at
the repository root and 17 keep it in a directory.** What predicts the split is
not fashion but how many images a repository builds:

| Images built | Where they go | Who does it |
|---|---|---|
| one | repository root | Grafana, Prometheus, Vault, Terraform, etcd, MinIO, Traefik, Airflow, Consul, InfluxDB, Thanos, Superset |
| several distinct services | each in its own directory | Jaeger `cmd/<binary>/`, Zitadel `apps/api/`, Immich `server/`, Sentry `self-hosted/` |
| many variants of the same binaries | one dedicated directory | Woodpecker `docker/` (seven), n8n `docker/images/`, Kubernetes `build/` |

The Go ecosystem answers it in writing: `golang-standards/project-layout` puts
container packaging in `/build/package` and compose files in `/deployments`, and
has no `/docker` at all.

**What the directory costs:** `docker build .` no longer finds the Dockerfile,
and Compose resolves relative paths and reads `.env` from the directory of the
first `-f` file rather than from the root. **What it buys:** one place for every
container concern and a root that stays readable. Both costs are paid once, in
the `Makefile` — `make image`, `make up`, `make down`, `make logs` — which is why
nothing here should be invoked with a raw `docker` command.

Growth is already decided: a second image becomes `docker/<name>/Dockerfile`, a
second local stack becomes `devenv/docker/<name>/`.

## Notebooks

`notebooks/` is split into two genres because they want opposite things from
version control.

- **`experiments/` — outputs stripped, enforced in CI.** Exploration runs against
  real inputs, and an output carries them into a history that does not forget.
  This is the cheapest leak channel in a repository and the one nobody watches.
- **`tutorials/` — outputs kept, data synthetic.** The reader wants to see what
  the code prints without running it. Ragas keeps outputs in every notebook under
  `docs/howtos/`; Phoenix does not enforce either way, and across its `tutorials/`
  some notebooks carry outputs and some do not — nothing says which was intended.

Ruff lints and formats `.ipynb` by default since 0.6, so notebooks are already
inside the gate. Mypy does not read them; that hole is real and named.

## What is deliberately **not** here

- **Release automation** — the publishing target (PyPI, an image, nothing at all)
  differs per project; twelve of thirteen surveyed repositories have it, and it
  is the first thing to add once you know where the artifact goes.
- **Coverage gate, `.importlinter`, `exclude-newer` cooldown** — all defensible,
  none decidable before there is code to measure, layer or pin.
- **A second image, a second local stack, `db/migrations` content** — created
  when earned, per the rules above. The rule is written down so the decision is
  not made twice.

## Honesty about what this is

This layout is **days old** and no product has been built on it yet. What is
solid is the survey underneath: the invariants were counted across real
repositories rather than inherited from a blog post. What is untested is every
choice the survey did not settle — and there are several, listed above.

**So the ask is not "adopt this". It is: where is this wrong?** Issues and pull
requests that disagree with a specific line, and say which repository does it
differently, are the most useful thing this can receive.

## Requirements

Python 3.14 and [uv](https://docs.astral.sh/uv/). Nothing else — `make install`
builds the environment from `uv.lock`, and no command in the `Makefile` needs an
activated virtualenv.

## License

MIT. See [LICENSE](LICENSE).
