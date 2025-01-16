import pytest
from app.nodes_and_edges.nodes.get_current_user import get_current_user
from app.states.text_2_sql import AgentState
from unittest.mock import patch

@pytest.fixture
def state():
    return AgentState()

def test_get_current_user(state):
    with patch('app.database.SessionLocal') as mock_session:
        mock_session.return_value.__enter__.return_value.query.return_value.filter.return_value.first.return_value = \
            type('User', (object,), {'name': 'Vinci'})()  # Mock user object
        config = {"configurable": {"current_user_id": 1}}
        result_state = get_current_user(state, config)
        assert result_state["current_user"] == "Vinci"
