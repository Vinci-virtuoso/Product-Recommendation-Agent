import pytest
from app.nodes_and_edges.nodes.human_readable_answer import generate_human_readable_answer
from app.states.text_2_sql import AgentState

def test_generate_human_readable_answer():
    state = AgentState({
        "sql_query": "SELECT * FROM users;",
        "query_result": "Found 3 matching products",
        "current_user": "Vinci",
        "query_rows": [
            {"ProductTitle": "Vinci's Shoes", "price": 100, "ImageURL": "url1"},
            {"ProductTitle": "Kuba's Shoes", "price": 150, "ImageURL": "url2"},
            {"ProductTitle": "Wale's Shoes", "price": 200, "ImageURL": "url3"}
        ]
    })
    
    result_state = generate_human_readable_answer(state)
    assert "Hello Vinci," in result_state["query_result"]
