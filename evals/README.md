# evals

Outside the package on purpose: judge prompts and datasets must not ship in the
wheel, they cost money, and they are not deterministic — so they must not run
under a plain `pytest`.

- `datasets/*.jsonl` — versioned cases; they diff as text.
- `evaluators/` — scorers and LLM judges.
- `thresholds.yaml` — the pass/fail contract as data, not logic buried in CI YAML.
- `gate.py` — exits non-zero when a threshold is breached. CI calls this.

Shape taken from Arize Phoenix.
