# agentic-python-template

The layout an agentic Python project starts from: the directories, the tooling
and a CI gate that is real — and nothing else. No framework, no opinions baked
into code, **zero dependencies**. Every placeholder that would need a library
(FastAPI, SQLAlchemy, LangGraph) ships its code commented out.

Placeholders say so in their names: `_your_product_`, `_your_agent_`,
`_your_tool_`, `_your_provider_`, `_your_resource_`.

## Start

1. **Use this template** on GitHub, then clone.
2. Rename `src/_your_product_/` to your package, and change `name` in
   `pyproject.toml` plus `[tool.hatch.build.targets.wheel] packages`.
3. `make install`
4. `make check` — must be green before you write anything.

## The tree

| Path | What lives there |
|---|---|
| `src/<product>/` | the one installable package — everything that ships |
| `src/<product>/llm/` | the single seam to the provider; nothing else imports an SDK |
| `src/<product>/agents/<name>/` | one directory per agent: `graph` `state` `prompts` `tools` |
| `src/<product>/tools/` | one file per tool; `__init__.py` is the registry |
| `src/<product>/db/` | all SQL — a query written elsewhere is a bug |
| `src/<product>/api/` | the web layer, a leaf: it imports the core, never the reverse |
| `src/<product>/retrieval/` | only if you do RAG; delete it otherwise |
| `tests/unit`, `tests/integration` | split by "does it need real I/O" |
| `evals/` | datasets, judges, thresholds and the gate — outside the package on purpose |
| `db/migrations/` | run by a migration tool, never imported by Python |
| `docker/`, `devenv/` | what ships, and what only ever runs on your machine |
| `notebooks/`, `examples/`, `scripts/`, `docs/` | developer-facing; not in the wheel |

## The gate

`make check` runs exactly what CI runs, in the same order:

```
ruff check .            find mistakes
ruff format --check .   one style, no arguments about it
mypy                    strict mode
pytest tests/unit
```

The first three are what all four official LangChain agent templates gate on.
The format check is our own addition — it costs one line and prevents "green on
my machine, red in CI".

## Why these directories

The reasoning behind every entry is being written from scratch after a research
pass over ~40 real trees disproved most of the previous version. Follow
[issue #3](https://github.com/lissdx/agentic-python-template/issues/3).

## Licence

MIT.
