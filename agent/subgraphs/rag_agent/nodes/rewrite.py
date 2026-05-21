from agent.core.model import model
from langchain_core.messages import SystemMessage, HumanMessage
from agent.core.shared_state import MessagesState
from agent.subgraphs.rag_agent.prompts import REWRITE_QUERY_SYSTEM_PROMPT

def rewrite(state: MessagesState):
    """Given user query which failed to retrieve proper documents, LLM rewrites the query in better terms for better retrieval"""
    
    
    query = state.get('rag_query')
    
    response = model.invoke([
        SystemMessage(content=REWRITE_QUERY_SYSTEM_PROMPT),
        HumanMessage(content=f"Query: \n{query}")
    ])
    
    rewritten = response.content.strip()
    print(f"   ↳ Rewritten Query: '{rewritten}'")

    
    return {
        'rag_query' : rewritten,
    }
    
    