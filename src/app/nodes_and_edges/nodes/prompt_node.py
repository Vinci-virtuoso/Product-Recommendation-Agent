from app.logic.prompt import create_chat_prompt_template


async def prompt_node(state):
    print("State in prompt:", state)
    question = state["question"]
    context = state["context"]
    formatted_context = [doc.page_content for doc in context]

    prompt = create_chat_prompt_template(context, question)

    state["prompt"] = await prompt.ainvoke(
        {"question": question, "context": formatted_context}
    )
    return state
