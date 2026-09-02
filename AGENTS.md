# Instructions for coding agents

Vendor-neutral: `CLAUDE.md` is a symlink to this file, so every tool reads one
source. What this repository is: [README.md](README.md).

## Before you create a file

This is a skeleton. Directories are the menu; the placeholder names
(`_your_product_`, `_your_agent_`, `_your_tool_`) mark what a project replaces.
Put a new file where the README table says it goes. If nothing fits, say so
instead of inventing a directory — the reasoning for each entry is being
rewritten under [issue #3](https://github.com/lissdx/agentic-python-template/issues/3).

Two boundaries are deliberate and must not be collapsed:

- **`agents/` decides, `tools/` acts.** A new capability is a tool; a new
  judgement is an agent.
- **The core never imports the web layer.** `api/` is a leaf.

## Rules

- **English only** — code, comments, docs, commit messages. No exceptions.
- **`uv` owns the environment.** Never `pip install` into `.venv`. `uv sync`
  after pulling, `uv add <pkg>` to add a dependency. `uv.lock` is committed and
  never hand-edited.
- **`pyproject.toml` is the only home for tool configuration.** No `setup.cfg`,
  no `.flake8`, no `mypy.ini`.
- **Tooling the repository needs goes in `[dependency-groups]`** (PEP 735),
  never in `[project.optional-dependencies]`.
- **The template has zero runtime dependencies.** Adding one is a decision, not
  a convenience — a stub that needs a library ships commented out instead.
- **The version has one source:** installed distribution metadata, read in
  `src/_your_product_/__init__.py`. Never a second literal.
- **Secrets appear in `.env.example` by name and never by value.**
- **No absolute paths anywhere in the repository.**

## Commands

`make help` lists them all. The ones that matter:

- `make check` — the whole gate, in CI order. Green here means green in CI.
- `make install` — sync the environment from `uv.lock`.
- `make image` — build the container image and prove it runs.
