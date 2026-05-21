from agent.core.shared_state import MessagesState
from langchain_core.messages import SystemMessage
from agent.core.model import model
from agent.tools.stock_info import get_stock_information
from agent.orchestrator.prompt import PLANNER_SYSTEM_PROMPT
from langchain_core.tools import tool

@tool
def rag_subgraph(query: str)->str:
    """Searches the Wells Fargo 2025 Annual Report for financial performance, net income, balance sheets, or annual report data."""
    pass

@tool
def web_search_agent(query: str)->str:
    """Searches the web for recent news, events, or general knowledge about any company or topic."""
    pass


tool_list = [rag_subgraph, web_search_agent, get_stock_information]
tool_list_names = {
    "search_wells_fargo_rag" : rag_subgraph,
    "get_stock_price" : get_stock_information,
    "search_web_tavily" : web_search_agent
}

planner_with_tool = model.bind_tools(tools=tool_list)



def planner(state: MessagesState):
    """The brain of the entire system which decides how to proceed ahead based on user query."""
    
    messages = state.get('messages', [])
    
    response = planner_with_tool.invoke([
        SystemMessage(content=PLANNER_SYSTEM_PROMPT ),
        *messages
    ])

    updates = {"messages": [response]}

    # Extract queries and store them directly in state variables
    if hasattr(response, 'tool_calls') and response.tool_calls:
        for tool_call in response.tool_calls:
            name = tool_call["name"]
            args = tool_call.get("args", {})
            if name == "rag_subgraph" and "query" in args:
                updates["rag_query"] = args["query"]
            elif name == "web_search_agent" and "query" in args:
                updates["tavily_query"] = args["query"]
            elif name == "get_stock_information" and "ticker" in args:
                updates["ticker"] = args["ticker"]
          
    
    
    return updates

