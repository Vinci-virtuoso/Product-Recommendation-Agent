from unittest.mock import patch, MagicMock
from langchain_core.messages import AIMessage
from app.nodes_and_edges.nodes.llm_node import llm_node


@patch("app.nodes_and_edges.nodes.llm_node.create_llm")
def test_llm_node(mock_create_llm, state):
    """
    Test the llm_node function with a mocked LLM.
    """
    # Mock the LLM instance
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Mocked AI response"
    mock_llm.invoke.return_value = mock_response
    mock_create_llm.return_value = mock_llm

    # Call the llm_node function
    updated_state = llm_node(state)

    # Assertions
    assert updated_state["answer"] == "Mocked AI response"
    assert updated_state["messages"][-1] == AIMessage(content="Mocked AI response")
    mock_llm.invoke.assert_called_once_with(state["messages"])
    mock_create_llm.assert_called_once()
