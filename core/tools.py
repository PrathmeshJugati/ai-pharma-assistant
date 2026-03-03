from core.retrieval import Retriever

def substitute_tool(query: str, retriever:Retriever):
    return retriever.find_substitute(query)

def search_tool(query: str,retriever:Retriever):
    return retriever.hybrid_search(query,alpha=0.9)

def followup_tool(query: str, memory, retriever:Retriever, session_id: str = "default"):
    return retriever.handle_followup(query, memory.get(session_id))

