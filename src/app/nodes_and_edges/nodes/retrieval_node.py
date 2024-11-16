from app.logic.retrieval import create_retriever
from app.database import db


def retrieve_node(state):
    print("State in retrieval node:", state)
    retriever = create_retriever(db, k=2)
    state["context"] = retriever.invoke(state["question"])
    return state
