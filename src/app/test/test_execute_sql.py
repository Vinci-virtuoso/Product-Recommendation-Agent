import pytest
from app.nodes_and_edges.nodes.execute_sql import execute_sql
from app.states.text_2_sql import AgentState
from unittest.mock import patch

@pytest.fixture
def state():
    return AgentState({"sql_query": "SELECT * FROM users;"})

def test_execute_sql(state):
    with patch('app.database.SessionLocal') as mock_session:
        mock_session.return_value.__enter__.return_value.execute.return_value.fetchall.return_value = [
            (1, 'Vinci', 25, 'alice@example.com'),
            (2, 'Kuba', 25, 'bob@example.com'),
            (3, 'Wale', 25, 'charlie@example.com')
        ]
        result_state = execute_sql(state)
        assert result_state["query_result"] == "Found 3 matching products"
        assert len(result_state["query_rows"]) == 3
