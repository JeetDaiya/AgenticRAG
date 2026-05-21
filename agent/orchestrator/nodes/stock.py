from langchain_core.messages import ToolMessage
import json
from agent.core.shared_state import MessagesState
from agent.tools.stock_info import get_stock_information


def stock_node(state: MessagesState):
    # 1. Retrieve the ticker stored by the planner
    # Read ticker from its own dedicated state field (written by planner)
    ticker = state.get("ticker")
    tool_call_id = None
    
    # Always scan the planner's last message to extract the correct tool_call_id
    last_message = state["messages"][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        for tc in last_message.tool_calls:
            if tc["name"] == "get_stock_information":
                if not ticker:
                    ticker = tc.get("args", {}).get("ticker")
                tool_call_id = tc.get("id")
                break
    
    if not ticker:
        return {"stock_info": {"error": "No ticker supplied"}}
        
    # 2. Invoke the tool function directly (preserving its rich return dict)
    result = get_stock_information.invoke({"ticker": ticker})
    
    # 3. Get the ToolMessage and attach the correct tool_call_id
    tool_msg = result.get("messages", [None])[0]
    if tool_msg and tool_call_id:
        tool_msg.tool_call_id = tool_call_id
    
    # 4. Return updates for both 'messages' and 'stock_info' state keys
    return {
        "messages": [tool_msg] if tool_msg else [],
        "stock_info": result.get("stock_info", {})
    }
