"""All SQL lives here. A query written outside this package is a bug.

Two `db` directories are deliberate: this one is Python access; db/migrations/ at
the repository root is run by a migration tool and never imported. That is onyx's
shape.
"""
