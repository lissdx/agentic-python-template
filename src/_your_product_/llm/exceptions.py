"""Errors this subsystem raises. Per-subsystem, the way onyx does it — it keeps
nine such modules and no central one, so a caller imports the vocabulary of the
subsystem it actually touches.
"""


class LLMError(Exception):
    """The provider seam failed: refusal, timeout, malformed output, budget."""
