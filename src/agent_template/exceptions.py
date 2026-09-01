"""The error taxonomy: one root, one module.

Four of the five surveyed repositories that have a taxonomy keep a single root
exception in one module; `browser-use` federates its hierarchy per subsystem.
The single root wins here because errors in an agentic system cross transports —
a tool failure surfaces in an HTTP handler, a CLI and a trace — and a caller that
wants "anything this package raised" should not have to import five modules.

Federate later if a subsystem grows its own vocabulary. That is a refactor, not
a rewrite: the federated classes still inherit from this root.
"""


class AgentTemplateError(Exception):
    """Base class for every error this package raises deliberately."""


class ConfigError(AgentTemplateError):
    """Configuration is missing, malformed, or contradicts itself."""


class ModelError(AgentTemplateError):
    """The provider seam failed: refusal, timeout, malformed output, budget."""


class ToolError(AgentTemplateError):
    """A tool could not complete the action it was asked to perform."""
