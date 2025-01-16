from app.states.text_2_sql import AgentState
from sqlalchemy import text
from app.database import SessionLocal
import logging

def execute_sql(state: AgentState):
    logging.basicConfig(level=logging.INFO)  # Set up logging
    sql_queries = state["sql_query"].strip().split(';')
    session = SessionLocal()
    print(f"Executing SQL queries: {sql_queries}")  # Log the SQL queries
    state["sql_query"] = sql_queries  # Log the SQL queries for debugging
    print(f"Current state before execution: {state}")  # Log the current state
    try:
        for query in sql_queries:
            if query.strip():
                result = session.execute(text(query.strip()))
                if query.lower().startswith("select"):
                    rows = result.fetchall()
                    if rows:
                        state["query_rows"] = [dict(zip(result.keys(), row)) for row in rows]
                        state["query_result"] = f"Found {len(rows)} matching products"
                    else:
                        state["query_rows"] = []
                        state["query_result"] = "No results found."
                else:
                    session.commit()
                    state["query_result"] = "Order placed successfully!"
        state["sql_error"] = False
    except Exception as e:
        state["query_result"] = f"Error executing SQL query: {str(e)}"
        print(f"Error executing SQL query: {str(e)}")  # Log the error for debugging
        state["sql_error"] = True
        print(f"Error executing SQL query: {str(e)}")
        session.rollback()
    finally:
        session.close()
    return state
