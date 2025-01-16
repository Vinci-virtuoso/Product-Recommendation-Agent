import pytest
from app.nodes_and_edges.nodes.end_max_iterations import end_max_iterations
from app.states.text_2_sql import AgentState

def test_end_max_iterations():
    state = AgentState()
    result_state = end_max_iterations(state)
    assert result_state["query_result"] == "Please try again."
