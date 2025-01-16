from app.states.text_2_sql import AgentState
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.config import RunnableConfig
from app.models.chat_models import ConvertToSQL
from app.database import engine
from app.logic.get_database_schema import get_database_schema



def convert_nl_to_sql(state: AgentState, config: RunnableConfig):
    question = state["question"]
    current_user = state["current_user"]
    schema = get_database_schema(engine)
    print(f"Converting question to SQL for user '{current_user}': {question}")
    
    system = """You are an assistant that converts natural language questions into SQL queries based on the following schema:

{schema}

The current user is '{current_user}'. For order insertions, follow these steps:
1. First, get the product details using a SELECT query
2. Then, create the order using INSERT
3. Use double quotes for string literals containing apostrophes
4. For product titles, use LIKE with wildcards to make the search more flexible
5. ALWAYS limit results to 5 products using 'LIMIT 5

Example order insertion:
INSERT INTO orders (user_id, order_date, total_amount)
SELECT 
    (SELECT id FROM users WHERE name = "current_user"),
    CURRENT_TIMESTAMP,
    p.price
FROM products p
WHERE p.ProductTitle LIKE "%product_name%";

Then insert the order item:
INSERT INTO order_items (order_id, product_id, quantity, price)
SELECT 
    last_insert_rowid(),
    p.ProductId,
    1,
    p.price
FROM products p
WHERE p.ProductTitle LIKE "%product_name%";

Provide only the SQL queries without any explanations.
""".format(schema=schema, current_user=current_user)
    
    convert_prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("human", "Question: {question}"),
    ])
    
    llm = ChatOpenAI(temperature=0)
    structured_llm = llm.with_structured_output(ConvertToSQL)
    sql_generator = convert_prompt | structured_llm
    result = sql_generator.invoke({"question": question})
    
    # Clean up the SQL query by replacing single quotes with double quotes for product titles
    sql_query = result.sql_query
    if "INSERT INTO orders" in sql_query:
        # Split multiple queries if present
        queries = sql_query.split(';')
        cleaned_queries = []
        for query in queries:
            if query.strip():
                # Replace problematic characters in product titles
                query = query.replace("'%", '"%')
                query = query.replace("%'", '%"')
                cleaned_queries.append(query)
        state["sql_query"] = '; '.join(cleaned_queries)
    else:
        state["sql_query"] = sql_query
        
    print(f"Generated SQL query: {state['sql_query']}")
    return state
