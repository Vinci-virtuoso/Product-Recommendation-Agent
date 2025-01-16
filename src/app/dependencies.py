from functools import lru_cache
from app.workflows.text2sql_workflow import text2sql_graph

@lru_cache()
def get_cached_text2sql_graph():
    return text2sql_graph()