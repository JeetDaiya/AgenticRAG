from agent.core.model import model
from agent.subgraphs.web_search_agent.prompts import WEB_SYNTHESIS_SYSTEM_PROMPT
from langchain_core.prompts import ChatPromptTemplate
from agent.core.shared_state import MessagesState

def web_result_formatter(state: MessagesState):
    """Given content of web results, LLM formats them into a detail response with citations"""

    news_data = state.get('news_data', '')
    user_query = state.get('user_query', '')
    prompt = ChatPromptTemplate(
        [
            ('system', WEB_SYNTHESIS_SYSTEM_PROMPT),
            ('human', "User Query: {user_query}\n\nNews Data: {news_data}")
        ]
    )
    
    chain = prompt | model
    
    response = chain.invoke({
        'user_query' : user_query,
        'news_data' : news_data
    })
    
    return {
        "news_data_formatted" : response.content
    }
    
    
    
    
    
