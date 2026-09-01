# agentic-python-template

A starting layout for an agentic Python project — the directory structure, the
tooling and the CI gate, with the reason for each decision written next to it.

**Use this template** → then:

```bash
make rename NAME=my-project    # renames the package everywhere, refreshes the lock
make install
make check                     # lint → typecheck → test, the order CI runs
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

## What is deliberately **not** here

An empty directory is a claim about a system that does not exist. The tree is
read as an architecture diagram, so it only contains subsystems that are real.

- **`memory/`, `persistence/`, `safety/`, `hitl/`, `gen/`, `simulations/`** —
  part of the layout when the subsystem exists. Create them then, with a
  docstring, not now.
- **`Dockerfile` / `docker-compose.yml`** — a container encodes a deployment
  shape this template cannot know, and an untested Dockerfile is worse than none.
- **Release automation** — publishing target (PyPI, an image, nothing at all)
  differs per project; twelve of thirteen surveyed repositories have it, and it
  is the first thing to add once you know where the artifact goes.
- **Coverage gate, `.importlinter`, `exclude-newer` cooldown** — all defensible,
  none decidable before there is code to measure, layer or pin.

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
