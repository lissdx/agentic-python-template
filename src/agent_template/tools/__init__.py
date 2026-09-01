"""The things that act. One file per tool.

A tool performs: it reads a mailbox, writes a row, calls an API. It does not
decide whether it should run — that is the agent's job.

Derive the tool's description from its argument schema rather than writing it
twice in prose: `browser-use` builds `prompt_description()` from
`model_json_schema()`, which makes prompt/schema drift structurally impossible
when a parameter is renamed.
"""
