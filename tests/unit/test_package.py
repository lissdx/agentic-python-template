"""Smoke test: the package imports and reports a version.

Its real job is to give CI something to run from day one, so the gate exists
before the code does rather than being added once it is already inconvenient.
"""

import agent_template


def test_package_exposes_a_version() -> None:
    assert isinstance(agent_template.__version__, str)
    assert agent_template.__version__
