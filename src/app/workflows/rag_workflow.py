from langgraph.graph import END, StateGraph

from app.nodes_and_edges.nodes.llm_node import llm_node
from app.nodes_and_edges.nodes.prompt_node import prompt_node
from app.nodes_and_edges.nodes.retrieval_node import retrieve_node
from app.states.rag_state import AgentState


def create_rag_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("generate_prompt", prompt_node)
    workflow.add_node("llm_node", llm_node)

    workflow.add_edge("retrieve", "generate_prompt")
    workflow.add_edge("generate_prompt", "llm_node")
    workflow.add_edge("llm_node", END)

    workflow.set_entry_point("retrieve")
    return workflow.compile()
