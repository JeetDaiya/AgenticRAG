from tavily import TavilyClient
from agent.core.shared_state import MessagesState
import os

tavily_client = TavilyClient(
    api_key=os.getenv('TAVILY_API_KEY')
)


def get_news(state: MessagesState):
    """Returns company's news based on the user's query."""
    tavily_query = state.get('tavily_query') or state.get('user_query')
    print(tavily_query)
    

    response = tavily_client.search(
        query= tavily_query,
        search_depth="advanced",
        max_results=5,
    )

    content = []

    for result in response.get("results", []):
        content.append(
            {
                "url": result.get("url", ""),
                "content": result.get("content"),
            }
        )
        
    formatted_news_string = '\n\n'.join([f"Source: {res.get('url', 'Unknown')}\n Content: {res.get('content', '')}" for res in content])

    if not formatted_news_string:
        formatted_news_string = "No recent news found for this company."

    # Return the nice string!
    return {"news_data": formatted_news_string}





