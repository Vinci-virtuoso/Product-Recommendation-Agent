from app.logic.prompt import create_chat_prompt_template


def prompt_node(state):
    print("State in prompt:", state)
    question = state["question"]
    context = state["context"]
    formatted_context = [doc.page_content for doc in context]

    prompt = create_chat_prompt_template(context, question)

    state["prompt"] = prompt.invoke(
        {"question": question, "context": formatted_context}
    )
    return state
