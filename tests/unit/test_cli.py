"""The entry point the container image runs actually runs."""

from agent_template.cli.__main__ import main


def test_main_exits_zero() -> None:
    assert main([]) == 0
