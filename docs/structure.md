# Project structure — what each thing is for

Every directory and every file in this repository, with the reason it exists.

**Who this is for.** Anyone — human or coding agent — who is holding a new file
and does not know where it goes, or is looking at an existing one and wants to
know whether it may be changed. It answers *where does this belong* and *may I
touch this*, not only *what is this*.

**How to read an entry.**

| Field | Answers |
|---|---|
| **What** | the thing itself, in one line |
| **Pain** | what breaks if it is missing — the reason it earns its place |
| **Belongs here if** | the test to apply when deciding where something goes |
| **Not here** | the mistake people actually make, and where that thing goes instead |
| **Why this way** | short: who else does it, where we copied it from |
| **Firmness** | `invariant` — do not change · `our choice` — arguable, argue with evidence · `open` — not decided yet |
| **Changes when** | the trigger that makes this decision expire |

Fields that would be noise for a given entry are left out. Numbers and sources
are collected once, at the end, rather than repeated in every entry.

---

## The one rule that decides almost everything

**What is needed at runtime lives inside the package. What is needed only by a
developer lives outside it.**

This is mechanical, not aesthetic. `pyproject.toml` declares what goes into the
wheel:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/agent_template"]
```

A directory at the repository root is not in that wheel, so an installed copy of
this project cannot import it. That single fact settles every argument about
placement: `evals/` is inside the package because the harness runs against the
live system; `tests/` is outside because it never ships.

A second rule covers everything containers touch: **what gets built and shipped
lives in `docker/`; what only ever runs on a developer's machine lives in
`devenv/`.** It is the same rule, one level up.

---

## Root — tooling

### `pyproject.toml`

- **What.** The only home for project metadata and every tool's configuration.
- **Pain.** Settings scattered across `setup.cfg`, `.flake8`, `mypy.ini` and
  `pytest.ini` drift apart, and nobody can answer "what does CI actually run".
- **Belongs here if** it configures a tool used in this repository. All of it.
- **Not here:** dependency versions of the resolved tree — those are `uv.lock`.
- **Why this way.** Universal in the repositories surveyed; the modern Python
  packaging standards (PEP 621, PEP 735, PEP 639) all target this file.
- **Firmness:** invariant.

### `uv.lock`

- **What.** The exact resolved dependency tree, committed.
- **Pain.** Without it, two machines install two different sets of packages and
  "works on mine" becomes unanswerable. CI runs `uv sync --locked`, which fails
  when this file is stale rather than quietly resolving something else.
- **Belongs here if** you added a dependency: run `uv add`, commit the lock.
- **Not here:** never hand-edit it.
- **Why this way.** Applications commit their lockfile; libraries usually do not.
  This is a template for applications.
- **Firmness:** invariant.

### `.python-version`

- **What.** The interpreter version `uv` picks up automatically.
- **Pain.** Otherwise every contributor guesses, and the guess differs from CI.
- **Firmness:** our choice — the floor is also declared in `requires-python`;
  this file makes the local default match it without being asked.

### `Makefile`

- **What.** The single entry point for every command, and the definition of what
  CI runs.
- **Pain.** Commands that live only in a CI file cannot be run locally, so people
  discover failures after pushing. `make check` is the CI order exactly, so a
  green terminal means a green pipeline.
- **Belongs here if** anyone would otherwise have to remember a flag. The docker
  and compose invocations in particular carry `-f` and `--project-directory`
  flags that are wrong to omit.
- **Not here:** logic. A target that grows past a few lines becomes a script in
  `scripts/`.
- **Firmness:** invariant. **Changes when:** never — targets get added, the file
  stays the front door.

### `.gitignore`

- **What.** What must never enter history.
- **Pain.** Deleting a file does not remove it from git history. Secrets, real
  data and someone else's vendored toolchain are all easier to keep out than to
  take back out.
- **Belongs here if** it is generated, secret, or not yours — caches, `.env`,
  credentials, agent toolchains such as `_bmad/` and `.claude/`.
- **Why this way.** The agent-toolchain lines exist because a coding-agent
  installer will happily write megabytes of its own catalogue into your public
  repository. Closed before the first install, not after.
- **Firmness:** invariant.

### `.env.example`

- **What.** Every environment variable the project reads, by name, with a comment
  and without a value.
- **Pain.** A variable nobody documented is a variable nobody can find; the code
  fails at runtime with a message about `None`.
- **Belongs here if** the code reads it, or Compose substitutes it.
- **Not here:** values. `.env` holds those and is ignored.
- **Firmness:** our choice — present in only five of thirteen surveyed
  repositories, and worth it anyway: it is the cheapest documentation in the tree.

---

## Root — documents

### `README.md`

- **What.** The shop window: what this is, how to start, the headline decisions,
  and a link to this document.
- **Pain.** A README that tries to hold every reason becomes a document nobody
  finishes, and the reasons rot because they are duplicated elsewhere.
- **Not here:** the per-directory reasoning. That is this file.
- **Firmness:** our choice. **Changes when:** it stops fitting on a couple of
  screens.

### `README.project.md`

- **What.** The README a generated project starts from — Pain, Goal, Termination
  criteria, How to run.
- **Pain.** "Use this template" would otherwise hand you a README describing the
  template rather than your project. `make rename` moves this file over the old
  one.
- **Why this way.** The four headings force the questions a project cannot answer
  later: what hurts, what it does, and how you will know it is finished.
- **Firmness:** our choice.

### `AGENTS.md`

- **What.** Instructions for coding agents: the layout, the conventions, what CI
  gates.
- **Pain.** Without one, every agent re-derives the conventions and each one
  derives them differently.
- **Belongs here if** an agent must obey it on every task. Keep it short and
  imperative — it is read constantly.
- **Not here:** long reasoning. Link to this document instead.
- **Why this way.** Twenty-four of twenty-five repositories in the survey have an
  agent-instruction file; the vendor-neutral name is the one that does not tie
  you to a single tool.
- **Firmness:** invariant.

### `CLAUDE.md`

- **What.** A symlink to `AGENTS.md`.
- **Pain.** Two real files drift, and the tool that reads the stale one behaves
  differently from the tool that reads the fresh one.
- **Why this way.** One source, many vendor filenames. Add another symlink when
  another tool wants its own name.
- **Firmness:** our choice.

### `CONTRIBUTING.md`

- **What.** How to set up, what must pass before a pull request, and how to
  disagree with the layout usefully.
- **Pain.** Otherwise reviewers repeat the same four comments forever.
- **Firmness:** our choice.

### `SECURITY.md`

- **What.** How to report a vulnerability, what must never be committed, and the
  two agent-specific surfaces: prompt injection is an input, and a tool is a
  capability boundary.
- **Pain.** For an agentic project the interesting risks are not in the
  dependency tree — they are that retrieved text can carry instructions, and that
  whatever a tool can do, the model can be argued into doing.
- **Firmness:** our choice.

### `LICENSE`

- **What.** MIT.
- **Pain.** Code without a licence is code nobody may legally reuse, including a
  future employer evaluating it.
- **Firmness:** our choice — change it per project before publishing.

---

## `src/agent_template/` — the package

Everything here ships in the wheel. Everything outside it does not. That is the
whole reason the directory exists.

### `src/agent_template/__init__.py`

- **What.** The package root. It reads the version from the installed
  distribution metadata.
- **Pain.** A hand-written `__version__ = "0.1.0"` is a second source of truth,
  and it is wrong the first time someone bumps `pyproject.toml` and forgets.
- **Firmness:** invariant — every repository surveyed has exactly one version
  source.

### `src/agent_template/py.typed`

- **What.** An empty marker file saying "this package ships type information".
- **Pain.** Without it, a type-checker in a project that installs yours silently
  treats your package as untyped, and every annotation you wrote stops helping
  anyone downstream.
- **Firmness:** invariant.

### `src/agent_template/exceptions.py`

- **What.** The error taxonomy: one root class, and the errors that inherit it.
- **Pain.** Without a root, a caller who wants "anything this package raised"
  has to enumerate classes from five modules and will miss the sixth.
- **Belongs here if** the code raises it deliberately.
- **Not here:** exceptions from libraries you call — wrap them, do not re-export.
- **Why this way.** Four of the five surveyed repositories with a taxonomy keep a
  single root in one module; `browser-use` federates per subsystem instead. The
  single root wins here because errors in an agentic system cross transports —
  a tool failure surfaces in an HTTP handler, a CLI and a trace.
- **Firmness:** our choice. **Changes when:** a subsystem grows its own
  vocabulary — then federate, keeping this class as the base.

### `src/agent_template/contracts/`

- **What.** Pydantic models: the vocabulary every other subpackage speaks.
- **Pain.** When each module defines its own shape of the same thing, the
  translation code between them is where the bugs live.
- **Belongs here if** it crosses a boundary — a request, a response, agent state,
  tool arguments, a stored record.
- **Not here:** behaviour. A model that opens a file or calls a provider has
  stopped being a contract; that logic belongs in the subpackage that owns it.
- **Why this way.** All thirteen surveyed repositories give schemas a defined
  home; the names differ (`entities/`, `views.py`), the fact does not.
- **Firmness:** invariant.

### `src/agent_template/agents/`

- **What.** The things that decide. One file per agent.
- **Pain.** An agent and a tool in the same file ship together, so a new
  capability forces a re-review of a judgement that did not change.
- **Belongs here if** it *chooses*: which tool to call, whether to answer, when
  to hand back to a human.
- **Not here:** the action itself → `tools/`. The prompt text → `prompts/`. The
  shape of its output → `contracts/`.
- **Why this way.** Taken from the LangChain agent-lifecycle workshop layout.
- **Firmness:** our choice. **Changes when:** nothing so far — the split holds at
  any size.

### `src/agent_template/tools/`

- **What.** The things that act. One file per tool.
- **Pain.** A tool that also decides whether it should run cannot be reused by a
  second agent with a different policy.
- **Belongs here if** it *performs*: reads a mailbox, writes a row, calls an API.
- **Not here:** the decision to call it → `agents/`.
- **Why this way.** Same source as `agents/`. Derive the tool's description from
  its argument schema rather than writing it twice — `browser-use` builds
  `prompt_description()` from `model_json_schema()`, which makes prompt/schema
  drift impossible when a parameter is renamed.
- **Firmness:** our choice.

### `src/agent_template/prompts/`

- **What.** Prompt text, loaded at runtime.
- **Pain.** A prompt buried in a Python string is invisible to whoever tunes it,
  and every edit is a code review. A prompt outside the package is not in the
  wheel, so the deployed service cannot find it.
- **Belongs here if** the model reads it.
- **Not here:** nothing goes elsewhere — but the split *inside* matters: long
  prompts are `.md` files read at import, one-line instructions are module
  constants. The test is whether a non-engineer would ever edit it without
  touching code.
- **Why this way.** Nine of thirteen surveyed repositories give prompts a
  defined location; the ones that do not are the ones whose prompts are one line.
- **Firmness:** our choice.

### `src/agent_template/model/`

- **What.** The single seam to the LLM provider. Nothing else imports a provider
  SDK.
- **Pain.** Without it, swapping a provider, adding a retry, capping a token
  budget or pinning a model version is a search-and-replace across the codebase —
  and the one call site you miss is the one that bills you.
- **Belongs here if** it talks to the model: client construction, retries,
  timeouts, token accounting, structured-output plumbing.
- **Not here:** the prompt → `prompts/`. What to do with the answer → the agent.
- **Why this way.** Present in **all thirteen** surveyed repositories — the
  strongest signal in the whole survey. Grep for the SDK name and this directory
  is the only hit.
- **Firmness:** invariant.

### `src/agent_template/obs/`

- **What.** Logging, tracing, metrics, cost.
- **Pain.** Without a trace you cannot answer why a run cost what it cost or
  which step chose wrongly — and after the run, the answer is gone. In an
  agentic system a run that quietly loops is green on every uptime check.
- **Belongs here if** it observes rather than does: logger setup, span helpers,
  token and latency accounting.
- **Why this way.** Twelve of thirteen surveyed repositories have it. It is not a
  late addition; retrofitting instrumentation means re-touching every call site.
- **Firmness:** invariant.

### `src/agent_template/config/`

- **What.** Settings, read once and validated at startup.
- **Pain.** A module that reaches into the environment mid-call cannot be tested
  without mutating the process, and a bad value is discovered in production
  rather than at boot.
- **Belongs here if** it reads configuration. Read it here, pass it down.
- **Not here:** the variable names for humans → `.env.example`.
- **Firmness:** invariant.

### `src/agent_template/cli/`

- **What.** Command-line entry points: parse, build, call, print.
- **Pain.** Logic that lives in a CLI cannot be imported or tested by anything
  else, so it gets copy-pasted the first time a second caller appears.
- **Belongs here if** it is wiring.
- **Not here:** anything worth a unit test → the subpackage it belongs to.
- **Firmness:** our choice — eight of thirteen have a CLI entry point.

### `src/agent_template/cli/__main__.py`

- **What.** Makes `python -m agent_template.cli` work; prints the version.
- **Pain.** The container image needs something to run. Without it, "the image
  works" is an assumption; with it, CI runs the image and the assumption becomes
  a command that exits zero.
- **Firmness:** our choice. **Changes when:** the project has a real entry point —
  replace the body, keep the file.

### `src/agent_template/evaluators/`

- **What.** The graders, as a library: given an output and a gold label, produce
  a score.
- **Pain.** An evaluator entangled with a dataset can only score that dataset,
  and cannot itself be unit-tested.
- **Belongs here if** it is called, not run: no side effects, no dataset, no
  opinion about which run it is scoring.
- **Not here:** the thing that loads data and drives the system → `evals/`.
- **Firmness:** our choice.

### `src/agent_template/evals/`

- **What.** The runs, as entry points: load a dataset, drive the system, apply
  the evaluators, report. Gold sets live here as data.
- **Pain.** `tests/` answers *does this code do what it was written to do*.
  Nothing answers *does the system still judge the way we judged* — until this
  exists. The two populations are different, not a hierarchy: the first is
  deterministic, the second is not.
- **Belongs here if** it needs the live system to produce a number.
- **Not here:** deterministic assertions about code → `tests/`. And note the
  direction: `tests/` contains tests *of* the eval code, which is why an eval
  cannot be a kind of test.
- **Why this way.** Inside the package because the harness is imported and run in
  a deployed environment, where a root-level directory is not importable. Both
  surveyed repositories that have tests *and* evals put evals inside the package.
  Build a gold set to defeat the obvious cheat — a set where string matching
  alone scores well measures nothing.
- **Firmness:** our choice — only five of thirteen have evals at all.

---

## `src/agent_template/` — the optional half

Five subpackages ship so that the layout is visible without cloning. **Each
one's docstring opens with the word `Optional.`, which is also the marker that
`make rename DROP_OPTIONAL=1` reads to delete them.** Keep the ones your system
has and delete the rest: the tree is read as an architecture diagram, and an
empty `hitl/` describes something that was never built.

### `src/agent_template/memory/` *(optional)*

- **What.** What the agent remembers across turns and across runs: history,
  summarisation, retrieved facts, the working set.
- **Pain.** Without a home, memory logic scatters into whichever agent needed it
  first and cannot be reused by the second.
- **Not here:** where it survives a restart → `persistence/`. Memory decides
  *what* is worth remembering; persistence decides *where it lives*.
- **Changes when:** the agent needs anything beyond a single run.

### `src/agent_template/persistence/` *(optional)*

- **What.** Durable state: checkpoints, run history, repositories over a store.
- **Pain.** When the storage engine is known in five places, changing it is five
  changes and one forgotten connection string.
- **Belongs here if** it knows the storage engine. The rest of the package asks
  for a repository, never for a connection.
- **Not here:** migrations → `db/migrations/`, outside the package, because a
  migration tool executes them and Python never imports them.

### `src/agent_template/safety/` *(optional)*

- **What.** Guardrails: input validation, output policy, refusal handling, PII
  redaction, budget caps.
- **Pain.** Policy expressed only in a prompt is a request, not a control — the
  model can be argued out of it.
- **Belongs here if** it runs *during* a request and can stop it. That is the
  boundary against `evaluators/`, and it is a boundary of **time**, not subject:
  a guardrail pays in latency and can prevent the outcome; an evaluator runs
  afterwards, pays in money, and can only record what already happened.
- **Changes when:** anything is checked before or after the model.

### `src/agent_template/hitl/` *(optional)*

- **What.** Human-in-the-loop: approval gates, escalation, the queue a person
  works through, and the resume path.
- **Pain.** Asking a human is easy; resuming correctly afterwards is not. Without
  a home for the state a run needs to continue from, the answer arrives with
  nothing to apply it to.
- **Changes when:** any decision is ever handed to a person.

### `src/agent_template/gen/` *(optional)*

- **What.** Output of code generators: API clients, protobuf stubs, typed
  schemas. Committed, never hand-edited, regenerated by a `make` target.
- **Pain.** Generated code that is not committed breaks a fresh clone; generated
  code that is hand-edited is silently overwritten.
- **Why inside the package.** It is imported at runtime, and a root-level `gen/`
  is not in the wheel. Engineers arriving from Go expect a root `gen/` — there
  the module resolves by path; here it would simply not be importable.
- **Changes when:** anything generates code into the tree.

---

## `tests/`

### `tests/`

- **What.** Everything that asserts the code does what it was written to do.
- **Pain.** Tests inside the package ship to every user of the library and slow
  every install; tests with no layout become one file nobody opens.
- **Belongs here if** it is deterministic and does not need the live system.
- **Not here:** anything scoring a model's judgement → `evals/`, inside the
  package.
- **Firmness:** invariant — all thirteen surveyed repositories organise tests.

### `tests/unit/`

- **What.** Fast, no I/O, run on every push.
- **Pain.** A suite that needs a database is a suite people stop running.
- **Files here:** `test_package.py` (the package imports and reports a version),
  `test_cli.py` (the command the image runs exits zero), `test_exceptions.py`
  (every error descends from one root). All three exist to give CI something to
  gate from day one, so the gate predates the code instead of being added when it
  is already inconvenient.

### `tests/integration/`

- **What.** Tests that need something real — a database, a container, a network.
- **Pain.** Mixed into `tests/unit/`, they make the fast suite slow and flaky, so
  people stop trusting a red build.
- **Belongs here if** it needs `make up` first.
- **Firmness:** our choice. **Changes when:** a third population appears — load
  tests get `tests/load/`.

---

## `docker/` — what gets built and shipped

### `docker/Dockerfile`

- **What.** A two-stage image build: install the environment with `uv`, then copy
  only what runs into a clean base. Runs unprivileged.
- **Pain.** Without a pinned, reproducible image, "it worked in CI" and "it works
  in production" are different statements. Running as root means whatever a tool
  can be argued into doing, it does as root.
- **Belongs here if** it defines something that ships.
- **Not here:** anything that only runs on a developer's machine → `devenv/`.
- **Why this way.** The `uv` invocation is the pattern from
  `fastapi/full-stack-fastapi-template`, which links every flag to the official
  `uv` Docker guide. Dependencies install from the lockfile *before* the source
  is copied, so editing code does not invalidate the dependency layer.
- **Firmness:** our choice, and a minority one — see *Sources*. **Changes when:**
  a second image appears; then each gets `docker/<name>/Dockerfile`.
- ⚠️ **Never call `docker build` by hand here** — it looks for a Dockerfile at
  the root of the context and will not find this one. `make image` carries `-f`.

### `docker/Dockerfile.dockerignore`

- **What.** What is kept out of the build context.
- **Pain.** Without it the local `.venv` and the whole `.git` history are
  uploaded to the daemon on every build — slow, and a path for secrets to reach
  an image layer.
- **Why the odd name.** Docker reads `.dockerignore` from the root of the *build
  context*, which is the repository root — not from beside the Dockerfile.
  BuildKit adds the alternative: an ignore-file named after its Dockerfile, in
  the Dockerfile's own directory, which takes precedence over the one at the
  context root. That is the only way to keep it next to the file it serves.
- **Firmness:** our choice, forced by putting the Dockerfile in a directory.
  Requires BuildKit — the default builder since Docker 23.

---

## `devenv/` — what only ever runs on your machine

### `devenv/`

- **What.** The development environment. Docker is one mechanism inside it, not
  the organising idea.
- **Pain.** Local scaffolding mixed with shipping artefacts means nobody can tell
  which compose file is for development and which is for deployment. Two surveyed
  repositories carry four and eight compose files at their root respectively, and
  the names do not say.
- **Belongs here if** it exists to make the project runnable locally — and that
  is not only containers: seed data, fixtures, a local cluster, a `direnv` file.
- **Why this way.** Grafana arranges it identically, in `devenv/docker/blocks/`.
- **Firmness:** our choice. **Changes when:** a second stack appears; then each
  gets `devenv/docker/<name>/`.

### `devenv/docker/compose.yaml`

- **What.** The local dependency stack: Postgres with pgvector, and the
  application service built from `docker/Dockerfile`.
- **Pain.** "Install Postgres and create a database" is a page of README that
  goes stale; one command that boots the same versions everywhere does not.
- **Belongs here if** the project needs it running to work locally.
- **Why pgvector.** The image ships Postgres with the extension already built,
  which is the difference between one line and a Dockerfile nobody wanted to
  write. Delete the service if the project has no database.
- **Firmness:** our choice — the *contents* are a starting guess, the *place* is
  not.
- ⚠️ **Every path in this file is written from the repository root**, because
  `make up` passes `--project-directory .`. Compose otherwise resolves relative
  paths — and reads `.env` — from the directory of the first `-f` file. Call it
  by hand and it silently looks in the wrong place.

### `devenv/docker/compose.override.yaml`

- **What.** Development-only settings, merged over the base file.
- **Pain.** Exposed ports, bind mounts and debug logging in the base file are
  either copied into deployment by accident or stripped out by hand every time.
- **Belongs here if** it is true only on a developer's machine.
- **Why this way.** Compose merges an override file over the base one; keeping
  the split means the base file never needs editing to run locally. The database
  port is deliberately not 5432 — that one is usually already taken by a Postgres
  someone installed and forgot.
- **Firmness:** our choice.

### `devenv/docker/postgres/init.sql`

- **What.** Runs once, when the database's data directory is first created:
  extensions, roles, schemas.
- **Pain.** An extension that must exist before the first migration has nowhere
  else to be created.
- **Not here:** table definitions → `db/migrations/`, where a migration tool can
  version them and roll them back. Postgres ignores this file on every later
  start, so anything that must be re-runnable does not belong in it.
- **Firmness:** our choice.

---

## `notebooks/`

### `notebooks/experiments/`

- **What.** Exploration: does this chunking work, why did the classifier miss
  this one.
- **Pain.** Exploration runs against real inputs, and a saved output carries them
  — an address, a fragment of a document, a key printed from the environment —
  into a history that does not forget. This is the cheapest leak channel in a
  repository and the one nobody watches.
- **Belongs here if** it is a question you are asking yourself.
- **Outputs are stripped, and CI enforces it.** `make notebooks-clean` before
  committing.
- **Naming.** A number for ordering, initials, a short description:
  `1.0-yl-chunking-window-sweep.ipynb`. The number sorts the history of an
  investigation with nobody maintaining an index.
- **Firmness:** our choice.

### `notebooks/tutorials/`

- **What.** Material for someone else to read and run.
- **Pain.** Stripping outputs here would remove exactly what the reader came for:
  seeing what the code prints without running it.
- **Belongs here if** it is an answer you are giving someone.
- **Outputs are kept — and the data is synthetic or public, never real.** That
  condition is what makes keeping them safe.
- **Firmness:** our choice. Note that `ruff` lints and formats `.ipynb` by
  default, so notebooks are already inside the gate; `mypy` does not read them,
  and that hole is real.

---

## Other top-level directories

### `db/migrations/`

- **What.** Schema history, executed by a migration tool.
- **Pain.** Schema changes applied by hand cannot be replayed on a new
  environment or rolled back on a bad one.
- **Belongs here if** it changes the schema. Whatever tool you pick, keep the
  pairing rule: everything that goes up must be able to come down.
- **Why outside the package.** A migration tool executes these; Python never
  imports them.
- **Firmness:** `open` — the tool is not chosen. Delete the directory if the
  project has no database.

### `docs/`

- **What.** Documentation for people working on the project.
- **Files here:** `structure.md` (this file), `architecture.md`,
  `runbook.md`.
- **Firmness:** our choice.

### `docs/architecture.md`

- **What.** The shape of the system: subsystems, seams, decisions and their
  costs, and what is not built yet.
- **Pain.** The one thing a reader cannot reconstruct from the code is what was
  rejected and why.
- **Not here:** where files go → this document. `architecture.md` is about the
  system; `structure.md` is about the repository.
- **Why this way.** Only five of thirteen surveyed repositories keep an
  architecture document, and almost none call it `ARCHITECTURE.md`: the function
  is real, the filename is not a convention.

### `docs/runbook.md`

- **What.** What an on-call reader needs at three in the morning: how it runs,
  how to tell it is healthy, failure modes, and how to roll back.
- **Pain.** An agent that writes to the outside world needs the rollback section
  answered *before* it is first deployed, not after.

### `examples/`

- **What.** Runnable scripts a reader can execute against a working install.
- **Pain.** A feature nobody can see working is a feature nobody adopts.
- **Belongs here if** it is small enough to read in one screen and does exactly
  one thing. A directory of half-maintained demos is worse than none — it is the
  first documentation to rot and the one readers trust longest.
- **Firmness:** our choice — eight of thirteen have it.

### `deploy/`

- **What.** Deployment manifests: compose files for deployment, Kubernetes
  objects, platform descriptors.
- **Pain.** A manifest encodes where the thing actually runs, and a wrong one is
  more expensive than a missing one — which is why this directory is empty here.
- **Not here:** the local stack → `devenv/`. This is the deployed one.
- **Firmness:** our choice — five of thirteen carry one.

### `scripts/`

- **What.** Repository automation that is too long for a `Makefile` target.
- **Belongs here if** the `Makefile` would otherwise grow logic.
- **Not here:** anything the application imports → the package.

### `scripts/rename_package.py`

- **What.** Turns the template into a project: rewrites the placeholder in three
  spellings, renames the package directory, swaps in the project README, removes
  every template-only artefact — including itself — and re-runs the formatter.
- **Pain.** GitHub's "Use this template" copies files and substitutes nothing.
  Without this, the first hour of every new project is renaming by hand across
  `pyproject.toml`, the source tree, the tests and the agent instructions.
- **Why the formatter runs afterwards.** A textual rename reorders symbols, and
  import sorting then fails the build. That was found by running it, not by
  reading it.
- **Firmness:** template-only. It deletes itself on first use.

### `scripts/check_notebook_outputs.py`

- **What.** Fails the build if a notebook under `notebooks/experiments/` carries
  outputs. `--fix` strips them.
- **Pain.** The leak channel described under `notebooks/experiments/`. A rule
  written in a README is a request; this is a gate.
- **Not here:** `notebooks/tutorials/` is deliberately not checked.
- **Firmness:** our choice.

---

## `.github/`

### `.github/workflows/ci.yml`

- **What.** The gate: `ruff check` → `ruff format --check` → `mypy --strict` →
  `pytest tests/unit` → the notebook-output check, plus a second job that builds
  the image and runs it.
- **Pain.** A check that nothing triggers is documentation. `uv sync --locked`
  additionally fails when the lockfile is stale, so a dependency added without
  relocking cannot reach `main`.
- **Belongs here if** it should block a merge. Anything worth enforcing goes into
  this file, not into a document as a request.
- **Why the type-checker matters most.** It fails the build in **all thirteen**
  surveyed repositories — the single strongest consensus found. A type-checker
  sitting in dev-dependencies is documentation.
- **Firmness:** invariant.

### `.github/workflows/template.yml`

- **What.** Runs `make rename` in both modes and then the full gate on the
  result, and asserts no template residue is left.
- **Pain.** "The template works" would otherwise be a sentence in a README.
- **Firmness:** template-only — the rename deletes this file, so a generated
  project does not inherit it.

### `.github/dependabot.yml`

- **What.** Weekly dependency updates for GitHub Actions and for `uv`.
- **Pain.** Pinned versions rot silently. This one answered within a minute of
  the first push: two actions were three major versions behind, inherited by
  copying a working CI file from another repository. That is how staleness
  spreads.
- **Firmness:** our choice — present in twelve of thirteen surveyed repositories.

---

## Two kinds of file that appear everywhere

### Local `README.md` files

`docker/README.md`, `devenv/README.md`, `notebooks/README.md`,
`db/migrations/README.md`, `deploy/README.md`, `examples/README.md`.

- **What.** A short sign at the door of a directory: what is inside, and a
  pointer to the entry above that explains why.
- **Pain.** Someone opening one directory in a file browser — or an agent given
  one path — sees no context at all. GitHub renders a directory's README
  automatically, so the sign costs nothing to display.
- **Belongs here if** the directory would otherwise be opened cold.
- **Not here:** the reasoning. **This document is the only place a rule is
  written.** A local README that starts explaining is a second copy that will
  drift; keep it to a few lines and a link.
- **Firmness:** our choice.

### `.gitkeep`

`notebooks/experiments/.gitkeep`, `notebooks/tutorials/.gitkeep`,
`tests/integration/.gitkeep`.

- **What.** An empty file whose only job is to make its directory exist in git.
- **Pain.** Git cannot store an empty directory. Without the marker the
  directory simply is not in a fresh clone, and the layout decision it
  represents disappears.
- **Belongs here if** the directory is part of the layout but has no content
  yet. Where the directory is a Python package, `__init__.py` does this job
  better — it holds a docstring saying what belongs there.
- **Firmness:** invariant, in the sense that git leaves no alternative.

---

## Landmines

Mechanical facts that break things. None of them are opinions.

| Trap | What actually happens |
|---|---|
| `docker build .` | Looks for `Dockerfile` at the context root and does not find ours. Use `make image`. |
| `docker compose up` by hand | Resolves relative paths **and reads `.env`** from the directory of the first `-f` file — `devenv/docker/`, not the root. Use `make up`. |
| An empty directory | Git cannot store one. A directory needs a file in it to exist at all — so the file may as well say why the directory does. |
| A configured directory with no `.py` files | `mypy` treats it as an error, not as empty. Removing the last script from `scripts/` breaks the build. |
| `.ipynb` files | `ruff` lints **and formats** them by default. A notebook can fail the lint gate. |
| A top-level directory you expect to import | It is not in the wheel. If it must be importable at runtime, it belongs inside the package. |
| Renaming a symbol across the tree | Import order changes, and the formatter check fails afterwards. Run `make format`. |

---

## Sources

The numbers quoted above come from two counts, both made by reading repository
trees rather than by asking.

**Thirteen repositories against one grid of thirty-eight surfaces** —
`pydantic/pydantic-ai`, `hynek/svcs`, `openai/openai-agents-python`,
`browser-use/browser-use`, `onyx-dot-app/onyx`, `langgenius/dify`,
`Arize-ai/phoenix`, `crewAIInc/crewAI`, `PrefectHQ/prefect`, `pydantic/pydantic`,
`astral-sh/uv`, `fastapi/full-stack-fastapi-template`,
`langchain-ai/react-agent`.

Present in all thirteen: a declared package manager, a linter/formatter, a
type-checker, **the type-checker gating CI**, an organised test layout, CI at
all, a single source for the version, a defined home for schemas, and one seam
that owns the conversation with the model provider.

Against the common advice: `src/` layout — **8 of 13**. A coverage gate —
**6 of 13**. A formal ADR directory — **0 of 13**.

**Forty-seven repositories on one question: where does the shipping Dockerfile
live** — **24 at the repository root, 17 in a directory.** What predicts it is
how many images the repository builds: one goes at the root (Grafana, Prometheus,
Vault, Terraform, etcd, MinIO, Traefik, Airflow, Consul, InfluxDB, Thanos,
Superset); several distinct services get one directory each (Jaeger
`cmd/<binary>/`, Zitadel `apps/api/`, Immich `server/`); many variants of the
same binaries get one dedicated directory (Woodpecker `docker/` with seven, n8n
`docker/images/`, Kubernetes `build/`).

The Go ecosystem answers it in writing: `golang-standards/project-layout` puts
container packaging in `/build/package` and compose files in `/deployments`, and
has no `/docker` at all.

**This repository is in the minority on that one**, deliberately, and the price
is listed under `docker/Dockerfile`.

**Other layouts worth reading:** `golang-standards/project-layout` documents
every directory with its rationale; `drivendataorg/cookiecutter-data-science`
keeps its reasoning in a separate `docs/opinions.md`; Grafana's `devenv/docker/blocks/`
is the local-environment pattern this repository copies.

---

## Honesty

This layout is young and no product has been built on it yet. What is solid is
the counting underneath it. What is untested is every choice the counts did not
settle — and those are marked `our choice` above, on purpose, so that arguing
with them needs evidence rather than permission.
