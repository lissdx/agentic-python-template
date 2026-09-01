"""Optional. Delete this package if the agent has no memory beyond one run.

What the agent remembers across turns and across runs: conversation history,
summarisation, retrieved facts, the working set carried between steps.

Kept apart from `persistence/`, which is about durability: memory decides *what*
is worth remembering, persistence decides *where it survives*. A system can have
either without the other.
"""
