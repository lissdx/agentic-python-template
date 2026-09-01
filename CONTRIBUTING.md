# Contributing

## Setup

Python 3.14 and [uv](https://docs.astral.sh/uv/) are the only prerequisites.

```bash
make install
make check
```

`make check` runs lint, type-check and tests in the order CI runs them, so a
green terminal means a green pipeline. No command needs an activated
virtualenv — `uv` resolves the environment itself.

## Before you open a pull request

- `make check` passes.
- New dependencies were added with `uv add` (or `uv add --group dev`) and
  `uv.lock` is committed. CI runs `uv sync --locked`, which fails on a stale
  lockfile rather than silently resolving a different tree.
- Tool configuration went into `pyproject.toml`. There is no second config file.
- Everything you wrote — code, comments, docs, commit messages — is in English.

## Disagreeing with the layout

That is the most useful contribution this repository can get, and it needs one
thing to be actionable: **name a repository that does it differently.** "This
should be flat" is an opinion; "`browser-use` federates its exception hierarchy
per subsystem, and here is why that beats a single root" is evidence.
