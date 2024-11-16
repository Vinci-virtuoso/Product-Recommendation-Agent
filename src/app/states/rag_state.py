from typing import TypedDict
from langchain_core.messages import BaseMessage
from langchain.schema import Document


class AgentState(TypedDict):
    question: str
    messages: list[BaseMessage]
    prompt: str
    context: list[Document]
    answer: str
    on_topic: str
