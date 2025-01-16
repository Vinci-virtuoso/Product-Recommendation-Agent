from app.dependencies import get_cached_text2sql_graph

try:
    graph = get_cached_text2sql_graph().get_graph()
    print(graph.draw_mermaid())
except Exception as e:
    print(f"Error displaying Mermaid diagram: {e}")
    pass
