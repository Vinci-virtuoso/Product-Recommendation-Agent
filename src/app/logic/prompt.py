from langchain_core.prompts import ChatPromptTemplate


def create_chat_prompt_template(context: str, question: str) -> ChatPromptTemplate:
    template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    return prompt
