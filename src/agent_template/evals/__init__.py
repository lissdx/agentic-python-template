"""The runs — entry points. Load a dataset, drive the system, apply evaluators, report.

Inside the package, not beside `tests/`, because the harness is imported and run
against the live system: a top-level directory is not in the wheel and therefore
not importable in a deployed environment.

`tests/` answers "does the code do what it was written to do". `evals/` answers
"does the system still judge the way we judged". Both are versioned; only the
first is deterministic.

Gold sets belong here as data. Build them to defeat the obvious cheat — a set
where string matching alone scores well measures nothing.
"""
