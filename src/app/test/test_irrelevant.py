import pytest
from app.nodes_and_edges.nodes.irrelevant import irrelevant
from app.states.text_2_sql import AgentState

def test_irrelevant():
    state = AgentState()
    result_state = irrelevant(state)
    assert result_state["query_result"] == "I am sorry I cannot answer your question."
