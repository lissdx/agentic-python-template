"""Which backend keeps the agent's state between steps.

Durability is not a top-level concern with its own directory — it is a
checkpointer, and a checkpointer is storage.
"""

# from langgraph.checkpoint.postgres import PostgresSaver
#
# def build(dsn: str) -> PostgresSaver:
#     return PostgresSaver.from_conn_string(dsn)
