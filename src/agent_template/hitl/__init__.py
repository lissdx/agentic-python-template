"""Optional. Delete this package if no decision is ever handed to a person.

Human-in-the-loop: approval gates, escalation, the queue a person works through,
and the resume path once they answer.

The hard part is not asking — it is resuming correctly afterwards. Whatever state
the run needs to continue from belongs here alongside the request, or the answer
arrives with nothing to apply it to.
"""
