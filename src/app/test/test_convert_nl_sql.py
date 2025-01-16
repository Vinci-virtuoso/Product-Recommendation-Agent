import pytest
from app.nodes_and_edges.nodes.convert_nl_sql import convert_nl_to_sql
from app.states.text_2_sql import AgentState
from unittest.mock import patch

@pytest.fixture
def state():
    return AgentState({"question": "Show me all men's shoes", "current_user": "Vinci"})

def test_convert_nl_to_sql(state):
    with patch('app.logic.get_database_schema.get_database_schema') as mock_schema:
        mock_schema.return_value = "Mocked schema"
        result = convert_nl_to_sql(state, None)
        assert "sql_query" in result
