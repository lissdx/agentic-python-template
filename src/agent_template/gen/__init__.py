"""Optional. Delete this package if nothing generates code into the tree.

Output of code generators: API clients, protobuf stubs, typed schemas. Committed,
never hand-edited, and reproducible by a `make` target that regenerates it.

Inside the package rather than at the repository root, because generated code is
imported at runtime and a top-level directory is not in the wheel. Engineers
arriving from Go expect a root `gen/`; there the module resolves by path, here it
would simply not be importable from an install.
"""
