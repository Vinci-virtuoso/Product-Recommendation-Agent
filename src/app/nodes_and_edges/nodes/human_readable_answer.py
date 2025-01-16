from app.states.text_2_sql import AgentState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def generate_human_readable_answer(state: AgentState):
    sql_queries = state["sql_query"]
    # Handle case where sql_query is a list
    sql = sql_queries[0] if isinstance(sql_queries, list) else sql_queries
    result = state["query_result"]
    current_user = state["current_user"]
    query_rows = state.get("query_rows", [])[:5]
    sql_error = state.get("sql_error", False)
    print("Generating a human-readable answer.")
    
    system = """You are an assistant that converts SQL query results into clear, natural language responses for a shopping store. 
    1. Start with a friendly greeting that includes the user's name
    2. For product recommendations: show product title, price, and image URL
    3. For order placement: provide a simple confirmation
    4. For order history: list past orders with dates and amounts
    5. Make the response visually organized and easy to read
    """
    
    if sql_error:
        # Error handling
        generate_prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", f"""SQL Query:
{sql}

Result:
{result}

Formulate a clear error message, starting with 'Hello {current_user},' and mention that no products were found.""")
        ])
    elif sql.lower().startswith("insert"):
        # Handle order placement confirmation
        generate_prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("human", f"""SQL Query:
{sql}

Result:
{result}

Format the response as a simple confirmation:
Hello {current_user}, your order has been successfully placed!""")
        ])
    elif sql.lower().startswith("select"):
        if not query_rows:
            # Handle no results
            generate_prompt = ChatPromptTemplate.from_messages([
                ("system", system),
                ("human", f"""SQL Query:
{sql}

Result:
{result}

Formulate a message stating no results were found, starting with 'Hello {current_user},'""")
            ])
        elif "orders" in sql.lower():
            # Handle order history display
            formatted_items = [f"Order placed on {row['order_date']} with total amount ${row['total_amount']}" for row in query_rows]
            items_string = "\n".join(formatted_items)
            generate_prompt = ChatPromptTemplate.from_messages([
                ("system", system),
                ("human", f"""SQL Query:
{sql}

Result:
{result}

Format the response as an order history:
Hello {current_user}, here are your recent orders:

{items_string}""")
            ])
        else:
            # Handle product recommendations
            formatted_items = [
                f"{i+1}. {row['ProductTitle']}\n   Price: ${row['price']}\n   Image: {row['ImageURL']}"
                for i, row in enumerate(query_rows[:5])
            ]
            items_string = "\n\n".join(formatted_items)
            total_found = len(state.get("query_rows", []))
            generate_prompt = ChatPromptTemplate.from_messages([
                ("system", system),
                ("human", f"""SQL Query:
{sql}

Result:
{result}

Format the response as product recommendations:
Hello {current_user}, here are 5 recommended products from {total_found} matches:

{items_string}

Would you like to see different products or get more details about any of these items?""")
            ])

    llm = ChatOpenAI(temperature=0)
    human_response = generate_prompt | llm | StrOutputParser()
    try:
        answer = human_response.invoke({})
        state["query_result"] = answer
        print("Generated human-readable answer.")
        return {"query_result": answer, **state}
    except Exception as e:
        print(f"Error generating human-readable answer: {str(e)}")
        state["query_result"] = "Sorry, I encountered an error while generating the response."
        return {"query_result": state["query_result"], **state}
