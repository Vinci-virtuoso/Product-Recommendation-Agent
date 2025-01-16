from langgraph.graph import END, StateGraph
from app.logic.relevance_router import relevance_router
from app.logic.execute_sql_router import execute_sql_router
from app.logic.check_attempts_router import check_attempts_router
from app.nodes_and_edges.nodes.get_current_user import get_current_user
from app.nodes_and_edges.nodes.check_relevance import check_relevance
from app.nodes_and_edges.nodes.convert_nl_sql import convert_nl_to_sql
from app.nodes_and_edges.nodes.execute_sql import execute_sql
from app.nodes_and_edges.nodes.human_readable_answer import generate_human_readable_answer
from app.nodes_and_edges.nodes.regenerate_query import regenerate_query
from app.nodes_and_edges.nodes.irrelevant import irrelevant
from app.nodes_and_edges.nodes.end_max_iterations import end_max_iterations
from app.states.text_2_sql import AgentState


import logging

def text2sql_graph():
    logging.basicConfig(level=logging.INFO) 
    workflow = StateGraph(AgentState)
    workflow.add_node("get_current_user", get_current_user)
    workflow.add_node("check_relevance", check_relevance)
    workflow.add_node("convert_to_sql", convert_nl_to_sql)
    workflow.add_node("execute_sql", execute_sql)
    workflow.add_node("generate_human_readable_answer", generate_human_readable_answer)
    workflow.add_node("regenerate_query", regenerate_query)
    workflow.add_node("irrelevant", irrelevant)
    workflow.add_node("end_max_iterations", end_max_iterations)

    workflow.add_edge("get_current_user", "check_relevance")

    workflow.add_conditional_edges(
        "check_relevance",
        relevance_router,
        {
            "convert_to_sql": "convert_to_sql",
            "irrelevant": "irrelevant",
        },
    )

    workflow.add_edge("convert_to_sql", "execute_sql")

    workflow.add_conditional_edges(
        "execute_sql",
        execute_sql_router,
        {
            "generate_human_readable_answer": "generate_human_readable_answer",
            "regenerate_query": "regenerate_query",
        },
    )

    workflow.add_conditional_edges(
        "regenerate_query",
        check_attempts_router,
        {
            "convert_to_sql": "convert_to_sql",
            "max_iterations": "end_max_iterations",
        },
    )

    workflow.add_edge("generate_human_readable_answer", END)
    workflow.add_edge("irrelevant", END)
    workflow.add_edge("end_max_iterations", END)

    workflow.set_entry_point("get_current_user")
    return workflow.compile()
