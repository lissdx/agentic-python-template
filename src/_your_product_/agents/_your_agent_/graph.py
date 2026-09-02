"""Builds and compiles the graph; exports `graph`. The one name a runner imports.

Live code needs LangGraph, which the template deliberately does not depend on —
uncomment and add the dependency when you start.
"""

# from langgraph.graph import END, START, StateGraph
#
# from .state import State
#
# def _answer(state: State) -> State:
#     return {"question": state["question"], "answer": ""}
#
# builder = StateGraph(State)
# builder.add_node("answer", _answer)
# builder.add_edge(START, "answer")
# builder.add_edge("answer", END)
# graph = builder.compile()
