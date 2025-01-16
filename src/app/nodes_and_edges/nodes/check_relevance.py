from app.states.text_2_sql import AgentState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.config import RunnableConfig
from app.logic.get_database_schema import get_database_schema
from app.database import engine
from app.models.chat_models import CheckRelevance


def check_relevance(state: AgentState, config: RunnableConfig):
    question = state["question"]
    schema = get_database_schema(engine)
    print(f"Checking relevance of the question: {question}")
    system = f"""You are an assistant that determines whether a given question is related to the following database schema.

Schema:
{schema}

A question is considered 'relevant' if it meets either of these criteria:
1. It relates to querying or accessing information from the database schema (products, orders, etc.)
2. It involves placing or managing orders

For example:
- "Show me all men's shoes" -> relevant (queries products)
- "Place an order for a red shirt" -> relevant (involves ordering)
- "What's the weather like?" -> not_relevant (unrelated to database or orders)

Respond with only "relevant" or "not_relevant".
"""
    human = f"Question: {question}"
    check_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", human),
        ]
    )
    llm = ChatOpenAI(temperature=0)
    structured_llm = llm.with_structured_output(CheckRelevance)
    relevance_checker = check_prompt | structured_llm
    relevance = relevance_checker.invoke({})
    state["relevance"] = relevance.relevance
    print(f"Relevance determined: {state['relevance']}")
    return state
