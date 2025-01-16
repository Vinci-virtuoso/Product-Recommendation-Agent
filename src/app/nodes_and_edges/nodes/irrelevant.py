from app.states.text_2_sql import AgentState

def irrelevant(state: AgentState):
    print("Generating a response for an irrelevant question.")
    state["query_result"] = "I am sorry I cannot answer your question."
    return state