"""The shared vocabulary: pydantic models every other subpackage speaks.

Belongs here: request/response shapes, agent state, tool arguments and results,
the schema of anything crossing a boundary.

Does not belong here: behaviour. A model that calls a provider or reads a file
has stopped being a contract. Contracts import nothing from this package, which
is what keeps the dependency graph acyclic without a linter enforcing it.
"""
