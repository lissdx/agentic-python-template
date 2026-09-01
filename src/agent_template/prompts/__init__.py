"""Prompt text, loaded at runtime.

Lives inside the package because it ships: a prompt the wheel cannot find is a
prompt the deployed service cannot use.

Split by length, not by taste. A long prompt is a `.md` file next to this module
and read at import; a one-line instruction is a module constant. The dividing
question is whether a non-engineer would ever edit it without touching code —
if yes, it is a file.
"""
