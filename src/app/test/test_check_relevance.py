import pytest
from app.nodes_and_edges.nodes.check_relevance import check_relevance
from app.states.text_2_sql import AgentState
from unittest.mock import patch

@pytest.fixture
def state():
    return AgentState({"question": "Show me all men's shoes"})

def test_check_relevance(state):
    with patch('app.logic.get_database_schema.get_database_schema') as mock_schema:
        mock_schema.return_value = "Mocked schema"
        result = check_relevance(state, None)
        assert result["relevance"] == "relevant"
