"""The graders — library code. Given an output and a gold label, produce a score.

An evaluator is called, never run. It has no dataset, no side effects and no
opinion about which run it is scoring, which is what makes it reusable across
eval sets and testable like any other function.

Separate from `evals/` for the same reason a test is not inside the code it
tests. Cross-ref: `tests/unit/` covers the evaluators themselves.
"""
