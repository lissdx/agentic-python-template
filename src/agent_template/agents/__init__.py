"""The things that decide. One file per agent.

An agent chooses: which tool to call, whether to answer, when to hand back to a
human. It owns a prompt, a set of tools and a stopping condition.

Kept apart from `tools/` because the two change for different reasons — a new
capability is a tool, a new judgement is an agent. Sharing a file couples two
release cadences that have no reason to move together.
"""
