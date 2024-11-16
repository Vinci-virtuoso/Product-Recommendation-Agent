from typing import TypedDict

from langchain.schema import Document
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    question: str
    messages: list[BaseMessage]
    prompt: str
    context: list[Document]
    answer: str
    on_topic: str
