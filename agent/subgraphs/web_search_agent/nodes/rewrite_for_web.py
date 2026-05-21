from agent.core.shared_state import MessagesState
from agent.core.model import model
from langchain_core.prompts import ChatPromptTemplate
from agent.subgraphs.web_search_agent.prompts import WEB_REWRITE_SYSTEM_PROMPT

def rewrite_for_web(state : MessagesState):
    query = state.get('tavily_query')
    
    prompt = ChatPromptTemplate([
        ('system', WEB_REWRITE_SYSTEM_PROMPT),
        ('human', '{query}')
    ])
    
    chain = prompt | model
    
    
    response = chain.invoke({
        'query' : query
    })
    
    return {
        'tavily_query' : response.content
    }
    
    
    
    