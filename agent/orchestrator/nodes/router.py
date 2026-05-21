from agent.core.shared_state import MessagesState

def route_from_planner(state: MessagesState):
    """
    Reads the output of the planner. 
    Returns a list of node names to execute in parallel, or routes to generate.
    """
    last_message = state["messages"][-1]
    
    # 1. Conversational Bypass
    # If the LLM didn't call any tools (e.g., user just said "hello"), go straight to generate
    if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
        return ["generate"]
    
    # 2. Fan-Out Setup
    # Create a list to hold every node we need to trigger
    destinations = []
    
    # 3. Check every tool the LLM requested and map it to your Graph Node names
    for tool_call in last_message.tool_calls:
        
        # Make sure these string names match the names you give your nodes in the Main Graph!
        if tool_call["name"] == "rag_subgraph":
            destinations.append("rag_agent_node")
        elif tool_call["name"] == "get_stock_information":
            destinations.append("stock_node")
        elif tool_call["name"] == "web_search_agent":
            destinations.append("web_agent_node")
    
    if not destinations:
        return ["generate"]
    
    
    return destinations