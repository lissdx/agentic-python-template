# Project structure

What goes where in an agentic Python project, and why — one section per path.

Written for two readers. A person asks *"where does this file go, and can I
argue with the answer?"* A coding agent asks the same thing and needs the answer
in a fixed shape it can parse. So every entry has the same four fields and the
tier is a field, never a hint buried in prose.

## How to read this

**Tier** — how firm the entry is. The bar is Google's, from the ADK recipe
handbook: a MUST is something *without which the recipe is broken*, not
something merely unusual.

| Tier | Meaning |
|---|---|
| **MUST** | Break this and something actually fails: the build, the wheel, the test run, or the ability of a reader to find code. |
| **SHOULD** | A convention with real weight behind it. Deviating is allowed and costs you something specific, named in the entry. |
| **MAY** | A menu item. Present because the alternative is invisible otherwise. Delete it if your system does not have the thing. |

**Who does it this way** — a link to a real tree, with a count where one was
taken. "Industry standard" with no name behind it is not an argument, and this
document does not make that claim anywhere.

**Two numbers you will see repeatedly.** They come from two counting passes and
are reproducible; the method is in [Where the numbers come from](#where-the-numbers-come-from).

> **This document has a defect on purpose, and it is worth naming.** The layout
> this repository takes its genre from,
> [golang-standards/project-layout](https://github.com/golang-standards/project-layout)
> (56 520★), lists nineteen directories in one flat list with no tiers. That
> omission is the subject of its most-reacted issue — 2 239 reactions — because
> readers began citing it as *the* Go standard and rejecting code that deviated.
> Tiers exist here so that cannot happen: most of this document is SHOULD.

## The one rule that decides almost everything

**What is needed at runtime lives inside the package. What is needed only by a
developer lives outside it.**

The boundary is enforced by the build, not by taste: only `src/_your_product_`
is listed under `[tool.hatch.build.targets.wheel]`, so a top-level directory is
not importable from an installed distribution. If you are unsure where something
goes, ask whether a user who ran `pip install your-product` needs it. Datasets,
judge prompts, notebooks and migrations: no. Prompts the agent sends at runtime:
yes.

The second rule, which decides the rest: **the direction of the arrow**. The
core never imports the web layer. `api/` is a leaf.

---

# Root

### `pyproject.toml`

- **Tier:** MUST
- **What.** Dependencies, build backend, and the configuration of every tool —
  ruff, mypy, pytest.
- **Why.** One home for tool configuration means one file to read and one file
  to diff. `setup.cfg`, `.flake8` and `mypy.ini` are the fragmentation this
  replaced.
- **Who does it this way.** Universal in the corpus. Tooling for the repository
  itself goes in `[dependency-groups]` (PEP 735), not
  `[project.optional-dependencies]` — the latter ships to whoever installs you.

### `uv.lock`

- **Tier:** MUST, committed
- **What.** The exact resolved dependency set.
- **Why.** `uv sync --locked` fails the build when the lock is stale instead of
  silently resolving something else. That is the difference between a
  reproducible CI run and a coincidence.
- **Never hand-edit it.**

### `Makefile`

- **Tier:** SHOULD
- **What.** The single entry point for every command, and the definition of what
  CI runs.
- **Why.** `make check` runs the gate in CI order, so a green terminal means a
  green pipeline. Without it the two drift: this repository's own siblings had a
  `check` target missing `ruff format --check` while CI ran it — green locally,
  red in CI.
- **Who does it this way.** All four official LangChain agent templates carry a
  Makefile; so do langchain, langgraph, phoenix, ragas, crewAI.
- **Deviation.** `just`, `poe`, or bare `uv run` in CI. The cost of bare `uv run`
  is the drift above.

### `README.md`

- **Tier:** MUST
- **What.** What this is, how to start, where the reasoning lives.
- **Not here.** Reasoning. It goes in this file. One fact, one home.

### `AGENTS.md` (with `CLAUDE.md` as a symlink)

- **Tier:** SHOULD
- **What.** Rules a coding agent must obey: commands, prohibitions, and a pointer
  here before it creates a file.
- **Why a symlink.** Vendor-neutral — every tool reads one source and no vendor's
  filename becomes the carrier.
- **Who does it this way.** 12 of 23 repositories measured (52%) — and **none of
  the four official LangChain templates**, and no vendor generator. That is why
  this is SHOULD and not MUST.
- **Not here.** The placement table. An agent that needs placement rules reads
  this file; duplicating them guarantees they diverge.

### `.env.example`

- **Tier:** MUST
- **What.** Every variable the code reads, by name, with a comment, without a
  value.
- **Why.** A variable that is not listed here is a variable nobody can find. It
  is also the only safe place for secrets to appear at all.

### `.python-version`, `.gitignore`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`

- **Tier:** `.gitignore` and `LICENSE` MUST; the rest SHOULD.
- **What.** Housekeeping. `.python-version` pins the interpreter `uv` picks.

### `Dockerfile` — root, or `docker/`?

- **Tier:** SHOULD — and this repository deviates from the majority on purpose.
- **The count.** Across 47 repositories with a shipping image: **24 keep the
  Dockerfile in the root, 17 keep it in a directory.** The root is the majority,
  not a consensus.
- **What this repository does.** `docker/Dockerfile`, with `compose.yaml` under
  `devenv/docker/`.
- **The price, stated plainly.** Every build needs `-f docker/Dockerfile`, every
  compose invocation needs `--project-directory .`, and the image is separated
  from the compose file that references it. Run both through `make` so nobody
  has to remember.
- **Who does it this way.** Netflix's dispatch and agent-service-toolkit keep a
  `docker/` directory. The Go world does the same under different names —
  `golang-standards` puts Docker under `/build/package` and compose under
  `/deployments`, which is why an engineer from Go rarely sees one in a root.
- **When the root wins.** One image, one compose file, nothing else. Then the
  extra hop buys nothing.

---

# Top-level directories

### `src/`

- **Tier:** MUST
- **What.** The layout that puts the package one directory down.
- **Why.** It decides one thing: whether you test the artifact you ship. With
  `src/`, an accidental import of the working copy cannot shadow the installed
  distribution, so `pytest` runs against what a user will get.
- **Who does it this way.** All four official LangChain agent templates, OpenAI
  agents, phoenix, ragas, mcp python-sdk.

### `tests/`

- **Tier:** MUST, and **outside** the package
- **What.** `unit/` and `integration/`, split by one question: does this test
  need real I/O — a network, a database, a live model?
- **Why outside.** Tests are not part of what ships. Inside the package they
  land in the wheel.
- **`tests/unit/__init__.py` and `tests/integration/__init__.py` are MUST.**
  Not style — without them pytest fails collection with *"import file mismatch"*
  as soon as the same file name exists in both tiers. All four official
  LangChain templates carry them.
- **`cassettes/`** — recorded model calls, so unit tests need no network. Used by
  the official react-agent and memory-agent templates.

### `evals/`

- **Tier:** SHOULD, and **outside** the package
- **What.** `datasets/*.jsonl`, `evaluators/`, `thresholds.yaml`, `gate.py`.
- **Why outside.** Three reasons, each sufficient: judge prompts and datasets
  must not ship in the wheel; evals cost money and are not deterministic, so
  they must not run under a plain `pytest`; and the pass/fail contract belongs in
  a data file that reviews on its own, not in CI YAML.
- **Who does it this way.** Shape taken from Arize Phoenix (`gate.py` +
  thresholds). Google ADK and agentos keep them outside too, by three different
  arrangements — but all outside.
- **Not here.** Anything imported at runtime.

### `data/`

- **Tier:** MAY — delete it if your project has no local working data
- **What.** The designated home for local inputs: the corpus you index,
  downloaded datasets, scratch data. Only `data/README.md` is committed;
  everything else is ignored by default (`data/*` + `!data/README.md` in
  `.gitignore`).
- **Why a default, not a prohibition.** The two mistakes are not symmetric.
  Accidentally committing private or third-party data is irreversible — history
  does not forget — while deliberately committing a small open sample costs one
  flag (`git add -f`). The default guards the irreversible side; the README
  names the reasons and leaves the decision with the developer.
- **Who does it this way.** cookiecutter-data-science (10 039★) ships `data/`
  in every generated project with `/data/` gitignored and the tree held by
  committed `.gitkeep` files. A README instead of `.gitkeep` is this
  repository's variant: a README can say why, a `.gitkeep` cannot.
- **Not here.** Evaluation datasets (`evals/datasets/`), fixtures a runnable
  example needs (`examples/`), seeds for the local stack (`devenv/`).

### `db/migrations/`

- **Tier:** MAY — delete it if you have no database
- **What.** Migration files, run by a migration tool.
- **Why at the root while `src/<product>/db/` also exists.** Two `db` directories
  are deliberate: this one is *run* by a tool and never imported by Python; the
  one inside the package is Python's access to the database.
- **Who does it this way.** onyx: `backend/onyx/db` for access, migrations
  separately.

### `docker/`

- **Tier:** SHOULD — see the Dockerfile entry above for the count and the price.
- **What.** The image and its `.dockerignore`. Note that BuildKit reads
  `<dockerfile-name>.dockerignore` from the Dockerfile's own directory, and that
  file takes precedence over a `.dockerignore` at the context root.

### `devenv/`

- **Tier:** MAY — this is the entry with the weakest external support in the
  whole document, and it is our own choice.
- **What.** Everything needed to run the project on a developer's machine and
  nowhere else: `docker/compose.yaml`, and later seeds, fixtures, kind configs.
- **The honest count.** `devenv/` has **zero precedents in the corpus**. The
  near-universal arrangement is `compose.yaml` in the root beside the
  `Dockerfile`, plus an override file.
- **Why we keep it.** `devenv` is the *concern* — the local environment — and
  docker is one mechanism inside it. The nesting reflects that, and the directory
  has somewhere to grow.
- **Who does something similar.** Grafana (`devenv/docker/blocks/`).

### `docs/`

- **Tier:** SHOULD
- **What.** This file, plus `architecture.md` (the why of the system) and
  `runbook.md` (what to do when it breaks).
- **Not here.** What goes where — that is this file, and this file is the only
  home for it.

### `notebooks/`

- **Tier:** MAY
- **What.** Two genres with **opposite** policies, which is the whole reason they
  are separated: `experiments/` strips outputs (real data must not enter a
  history that does not forget); `tutorials/` keeps them (seeing the output
  without running the code is the point) and uses synthetic data only.
- **Who shows the cost of not deciding.** Ragas ships outputs in all six
  notebooks reviewed; Phoenix is inconsistent within a single directory. That
  inconsistency is what an unwritten policy looks like.
- **Naming.** Sortable: `1.0-yl-retrieval-spike.ipynb`.

### `scripts/`

- **Tier:** MAY
- **What.** One-off operational scripts: a backfill, a dump, a migration helper.
- **The rule that defines it.** Nothing under `src/` imports anything here. A
  script that grows a second caller belongs in the package.
- **Trap.** Do not list `scripts` in mypy's `files` while it holds no Python —
  an empty entry fails the run.

### `examples/`

- **Tier:** MAY
- **What.** Runnable usage a reader can copy. Not tests, not documentation prose.

### `.github/`

- **Tier:** MUST for a repository anyone else will open
- **What.** `workflows/ci.yml` and `dependabot.yml`.
- **Why dependabot.** Pinned action versions rot silently. It answered within a
  minute of this repository's first push with three major-version gaps.

---

# `src/_your_product_/` — the package

One installable package, named after the product. Not `app`, not `pkg`, not
`core`. Split **by subsystem**, not by domain: the criterion for domain slicing
is a *conflict of models*, not size, and one agent product does not have one.
onyx — 31 877★, the largest open agentic product with a real business — keeps 40
top-level packages and not one domain name. Layer names at the top level:
**0 of 10** trees.

### `__init__.py`

- **Tier:** MUST
- **What.** The version, read from installed distribution metadata.
- **Why.** One source for the number. A `__version__` literal beside a version in
  `pyproject.toml` is two sources that will disagree.

### `py.typed`

- **Tier:** MUST if you ship types
- **What.** An empty marker (PEP 561) telling a consumer's type-checker that the
  annotations in this package are real.

### `config.py`

- **Tier:** SHOULD
- **What.** The only module that reads the environment. Everything else takes
  arguments.
- **Why a module, not a package.** It becomes a package when it has a second
  file, not before.
- **Who does it this way.** 15 of 19 repositories measured carry a
  `config.py`/`settings.py`. Production projects put pydantic-settings here.
- **The failure it prevents.** A module that reaches for `os.environ` mid-call
  cannot be tested without mutating the process.

### `cli.py`

- **Tier:** MAY — only if your project has a terminal command
- **What.** A thin shell: parse, build, call, print.
- **Who does it this way.** 13 of 19 measured. It is common, not universal, and
  the split is exactly "does this project have a command".
- **Why it is worth keeping in a skeleton anyway.** It gives the container image
  something to run, which turns *"the image works"* from an assumption into a
  command that exits zero.

### `observability.py`

- **Tier:** SHOULD
- **What.** Where logs, traces, and cost/latency accounting are configured —
  once, at startup.
- **Why.** Without it an agent is a black box: it answered, and why is
  unrecoverable after the run. This is not a late addition to an agentic system.
- **On the name.** Only 8 of 19 measured have a file called
  `observability`/`telemetry`/`tracing`. The *concern* is nearly universal; the
  *name* is not. onyx has seven such modules, dify three, phoenix three.
- **A module until a second backend arrives**, then `tracing/`.

### `llm/`

- **Tier:** MUST — the strongest convention found anywhere in the corpus
- **What.** The single seam to the provider: `base.py` (the Protocol every
  provider implements), `factory.py` (name to client — the one place a model is
  chosen), one file per vendor.
- **The count.** A dedicated provider seam appears in **9 of 10** trees. Nothing
  else in this document has that level of agreement.
- **Why the name `llm/` and not `models/`.** `models/` is the majority name in
  *libraries*, but in any project that also has a database the word already means
  "tables". `llm/` is confirmed at onyx (31 877★) and browser-use (111 925★).
- **The payoff.** Swapping a provider, adding a retry, capping a token budget or
  pinning a model version is one file — and grepping for the SDK name returns
  exactly this directory.
- **Not here.** Prompts. What to do with the answer.

### `agents/<name>/`

- **Tier:** MUST
- **What.** One directory per agent, four files with the same names in every one:
  `graph.py` (builds and compiles; exports `graph`), `state.py` (the typed state
  schema), `prompts.py` (this agent's prompts), `tools.py` (tools only this agent
  uses).
- **Why prompts live here and not in a central `prompts/`.** A prompt and the
  node that sends it change in the same commit. Splitting them puts one agent in
  two directories. All four official LangChain templates do it this way, and
  Google ADK's examples contain 85 `prompt.py` files sitting beside their agents.
- **When a central `prompts/` earns its place.** From roughly five agents on,
  when the question *"show me every prompt in the system"* becomes real. onyx and
  ragflow have one; they are answering that question, not this one.
- **Not here.** The action itself — that is a tool.

### `tools/`

- **Tier:** MUST
- **What.** One file per tool, plus `interface.py` (the contract) and
  `__init__.py` as the **registry** — the single place a tool becomes visible.
- **The boundary against `agents/`.** An agent *decides*; a tool *acts*. They
  change for different reasons — a new capability is a tool, a new judgement is
  an agent — so they do not share a file.
- **The count.** `tools/` is the most common directory name in the whole corpus:
  65 408 hits by code search, against 35 264 for `agents/`.
- **Test them without a graph.** That is the point of one file per tool.

### `db/`

- **Tier:** MAY — delete it if you have no database
- **What.** All SQL. `models.py` (tables — *not* request schemas), `session.py`,
  `checkpointer.py` (which backend keeps agent state between steps).
- **The rule.** A query written outside this directory is a bug.
- **Why durability has no directory of its own.** Durability *is* a checkpointer,
  and a checkpointer is storage. It appears as a separate top-level concern in
  1 of 10 trees.
- **Who does it this way.** onyx: `backend/onyx/db` for access, migrations kept
  separately at the root.

### `api/`

- **Tier:** MAY — only if you expose HTTP
- **What.** A leaf: `app.py` (`create_app()` and the ASGI object), `deps.py`,
  `schemas.py` (request/response models — *not* database tables),
  `routes/<resource>.py`.
- **The rule is the direction of the arrow, not the location.** The core imports
  nothing from here; this imports the core.
- **How to enforce it cheaply.** An import-linter contract —
  `agents/**` and `llm/**` must not import `fastapi`. dify carries 23 such
  contracts. A rule with nothing to check it drifts.
- **Note on middleware.** FastAPI middleware (HTTP request/response) belongs
  here. LangChain's agent middleware is a different thing under the same word —
  it wraps model and tool calls — and belongs beside the agent. Do not put them
  in one directory.

### `retrieval/`

- **Tier:** MAY — only if you do RAG
- **What.** Loaders, chunking, the vector-store client.
- **Delete it otherwise.** An empty concern in the tree reads as a concern the
  project has.

### `exceptions.py` — per subsystem, not central

- **Tier:** SHOULD
- **What.** Each subsystem keeps its own errors beside the code that raises them:
  `llm/exceptions.py`, `tools/exceptions.py`.
- **The count.** A single `exceptions.py` at the package root appears in 17 of 30
  repositories measured — but the large products do the opposite and federate:
  **onyx 9 modules, dify 20, airflow 20, sentry 20, posthog 20**. The root file
  is what small packages have; per-subsystem is what products grow into. This
  repository follows onyx.
- **A directory instead of a file?** Rare, and almost always deep inside a
  subsystem rather than at the top: sentry, crewAI, dify, phoenix. The one
  counter-example worth knowing is `google/adk-python`, which keeps
  `src/google/adk/errors/` as a package at the top and has no file at all.
- **When to switch.** When one subsystem's errors outgrow one module.

---

# Directories you should not have

Each of these was in an earlier draft of this repository and was removed after
being counted. They are listed because a name that sounds reasonable is the
hardest kind of mistake to see.

| Directory | Why not | The count |
|---|---|---|
| `obs/` | Invented abbreviation. Use `observability.py`. | **0** occurrences in 18 trees; 63 hits by code search against 65 408 for `tools/` |
| `model/` | Ambiguous with database models; the seam is `llm/`. | 0 in the same 18 trees |
| `contracts/` | The type belongs beside the seam it describes: `llm/base.py`, `tools/interface.py`, `db/models.py`, `api/schemas.py`. | present in **exactly one** repository of the corpus — 43★, one author |
| `evaluators/` beside `evals/` | Two directories always edited together are one directory. Phoenix nests them: `evals/.../evaluators/`. | no tree in the corpus has both as siblings |
| `evals/` **inside** the package | Judge prompts and datasets get baked into the wheel. | every corpus tree that has evals keeps them outside |
| `prompts/` beside `agents/` | Splits one agent across two directories. | see the `agents/` entry |
| `hitl/`, `safety/`, `guardrails/` | Interception points around the agent loop, not subsystems. | HITL 3 of 10, guardrails 2 of 10; browser-use at 111 925★ has neither |
| `persistence/` + `memory/` as siblings | Two directories for one store. | durability appears as its own concern in 1 of 10 |
| `gen/` | Generated output; no precedent and no writable rule for what belongs in it. | **0** in 40 trees |
| `deploy/` | Appears before there is anything to deploy. | 5 of 13 in one slice, unused in ours |

---

# Traps

Mechanical failures that do not depend on anyone's opinion. Four of these were
found by running a toolchain over the tree, not by reading it.

1. **`tests/<tier>/__init__.py` is required.** Without it pytest fails collection
   with *"import file mismatch"* the moment the same file name exists in two
   tiers.
2. **An empty directory in mypy's `files` fails the run.** If `scripts/` holds
   only a README, it must not be listed.
3. **`per-file-ignores` must cover `evals/*` and `notebooks/*`** if your rule set
   includes `T201` (`print` found) — otherwise the harness this document
   prescribes fails the linter this document prescribes.
4. **Compose resolves relative paths and `.env` against the *project directory*,**
   which defaults to the directory of the first `-f` file. A compose file under
   `devenv/docker/` therefore needs `--project-directory .` or every path in it
   silently means something else.
5. **`<dockerfile-name>.dockerignore` beside the Dockerfile wins** over a
   `.dockerignore` at the context root. Put the ignore file next to the
   Dockerfile it belongs to.
6. **The `__init__.py`-everywhere rule is folklore.** Implicit namespace
   subpackages *do* land in the wheel under both hatchling and setuptools, and
   `mypy --strict` is indifferent to them. Add `__init__.py` because it is
   conventional and because a package needs a docstring — not because packaging
   requires it.
7. **Renaming the package breaks import sorting.** Any rename must be followed by
   `ruff check --fix` and the full gate, not by a search and replace alone.

---

# The gate

`make check` runs what CI runs, in the same order.

| Step | Tier | Who does it this way |
|---|---|---|
| `ruff check .` | **MUST** | all four official LangChain agent templates, plus the FastAPI full-stack template |
| `mypy --strict` | **MUST** | all four templates run literally `mypy --strict src/` |
| `pytest tests/unit` | **MUST** | all four templates |
| `ruff format --check .` | **SHOULD** | **none** of the four agent templates; the FastAPI full-stack template does (`mypy` → `ty check` → `ruff check` → `ruff format --check`) |

The format check is this repository's own addition, and the tier says so. It
costs one line and prevents the failure its absence already produced in two
sibling repositories: a `make check` without it, next to a CI that had it —
green locally, red in CI.

Worth knowing about the gap: all four official templates also run **codespell**,
and the FastAPI template runs **typos**. A spell-check gate is more common in
this genre than a format gate. This repository has neither codespell nor an
import-linter contract yet.

---

# Where the numbers come from

Two counting passes, both against real trees via the GitHub trees API
(`repos/{owner}/{repo}/git/trees/HEAD?recursive=1`), not against blog posts.

- **Pass one (structure).** ~40 trees, read as trees; five adversarial checks and
  a completeness critic that built the proposed layout and ran a toolchain over
  it. This is where the counts for `llm/`, `contracts/`, HITL/guardrails/
  durability, `obs/`, `gen/` and the 24/17 Dockerfile split come from.
- **Pass two (files and toolchain).** 30 repositories for the exceptions count,
  19 for `config`/`cli`/`observability`, and the four official LangChain agent
  templates plus `fastapi/full-stack-fastapi-template` read line by line for the
  gate. Corpus: onyx, browser-use, dify, ragflow, agno, langchain, langgraph,
  pydantic-ai, openai-agents-python, phoenix, adk-python, ragas, crewAI,
  llama_index, autogen, OpenHands, mcp python-sdk, smolagents, django, starlette,
  flask, requests, sqlalchemy, pydantic, httpx, fastapi, airflow, sentry,
  posthog.

**A caution about a source you will meet.** `zhanymkanov/fastapi-best-practices`
(18 006★) attributes `router.py`, `schemas.py` and `dependencies.py` to Netflix's
dispatch. dispatch contains **none** of those file names — it has 68 `service.py`
and 65 `models.py` — and the repository is archived. Popular is not verified.

---

# Open questions

Written down rather than decided, so the same argument is not had twice.

- **`middleware/`.** LangChain v1 makes HITL, PII redaction, call limits and
  context compaction first-class middleware modules. This tree has no home for
  them. Deferred deliberately until a project needs one.
- **`db/` versus `storage/` inside the package.** `db/` was chosen; the objection
  that the tree then contains two directories called `db` stands.
- **Splitting `notebooks/` into `experiments/` and `tutorials/`.** No corpus tree
  does this, and "tutorials" is arguably documentation. Kept because the two
  genres have opposite output policies and mixing them has a visible cost.
- **`devenv/`.** Zero precedents. Kept as a considered choice; see its entry.

---

# Honesty

There is no industry standard for the layout of a Python agent project. Agreement
in real trees is narrow: one installable package split by subsystem, a dedicated
provider seam, tests outside the package split by whether they need real I/O, and
a web layer that is a leaf. Everything else — evals, prompts, HITL, guardrails,
durability — is contested, and any document claiming consensus there is inventing
it.

The closest thing to a real prescriptive layout for Python agents is
[google/adk-samples](https://github.com/google/adk-samples) —
`docs/recipe-handbook/languages/python.md`, 10 265★, and it is checked by a
command (`uv run validate`) rather than by prose.

Counts age. The passes above were taken in September 2026; treat anything older
than about six months as needing a re-count.
