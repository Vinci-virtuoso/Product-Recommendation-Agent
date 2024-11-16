from unittest.mock import patch, MagicMock
from app.nodes_and_edges.nodes.prompt_node import prompt_node
from unittest.mock import call


@patch("app.nodes_and_edges.nodes.prompt_node.create_chat_prompt_template")
@patch("app.nodes_and_edges.nodes.prompt_node.format_document")
def test_prompt_node(mock_format_document, mock_create_chat_prompt_template, state):
    mock_format_document.side_effect = lambda doc: f"Formatted {doc.page_content}"

    mock_prompt_template = MagicMock()
    mock_prompt_template.invoke.return_value = "Mocked Prompt"
    mock_create_chat_prompt_template.return_value = mock_prompt_template

    updated_state = prompt_node(state)

    assert updated_state["prompt"] == "Mocked Prompt"
    mock_format_document.assert_has_calls([call(doc) for doc in state["context"]])
    mock_create_chat_prompt_template.assert_called_once_with(
        state["context"], state["question"]
    )
    mock_prompt_template.invoke.assert_called_once_with(
        {
            "question": state["question"],
            "context": ["Formatted test1", "Formatted test2"],
        }
    )
