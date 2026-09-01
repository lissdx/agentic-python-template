"""The taxonomy holds: every error this package raises has one catchable root."""

import pytest

from agent_template.exceptions import (
    AgentTemplateError,
    ConfigError,
    ModelError,
    ToolError,
)


@pytest.mark.parametrize("error", [ConfigError, ModelError, ToolError])
def test_every_error_descends_from_the_root(error: type[AgentTemplateError]) -> None:
    assert issubclass(error, AgentTemplateError)
