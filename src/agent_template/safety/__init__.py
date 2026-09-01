"""Optional. Delete this package if nothing is checked before or after the model.

Guardrails: what runs *during* a request and can stop it — input validation,
output policy, refusal handling, PII redaction, budget caps.

The boundary against `evaluators/` is time, not subject matter. A guardrail runs
inside the request, pays for itself in latency, and can prevent the outcome. An
evaluator runs after, pays in money, and can only record what already happened.
"""
