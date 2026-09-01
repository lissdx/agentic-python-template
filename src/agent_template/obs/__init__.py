"""Logging, tracing, metrics, cost.

Belongs here: logger configuration, the tracer/span helpers, token and latency
accounting.

Instrumentation is not a late addition to an agentic system — without a trace
you cannot answer why a run cost what it cost or which step chose wrongly, and
the answer is unrecoverable after the fact.
"""
