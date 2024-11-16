from unittest.mock import patch, MagicMock
from app.nodes_and_edges.nodes.retrieval_node import retrieve_node


@patch("app.nodes_and_edges.nodes.retrieval_node.create_retriever")
@patch("app.nodes_and_edges.nodes.retrieval_node.db")
def test_retrieve_node(mock_db, mock_create_retriever, state):
    """
    Test the retrieve_node function with mocked dependencies.
    """
    # Mock the retriever's invoke method
    mock_retriever = MagicMock()
    mock_retriever.invoke.return_value = [
        {"title": "Document 1", "content": "Content of Document 1"},
        {"title": "Document 2", "content": "Content of Document 2"},
    ]
    mock_create_retriever.return_value = mock_retriever

    # Call the retrieve_node function
    updated_state = retrieve_node(state)

    # Assertions
    assert updated_state["documents"] == [
        {"title": "Document 1", "content": "Content of Document 1"},
        {"title": "Document 2", "content": "Content of Document 2"},
    ]
    mock_create_retriever.assert_called_once_with(mock_db, k=2)
    mock_retriever.invoke.assert_called_once_with(state["question"])
