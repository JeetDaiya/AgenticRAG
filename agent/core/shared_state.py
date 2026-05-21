from agent.core.pydantic_models.report_model import FinalReport
import operator
from typing import Annotated, List, TypedDict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

def merge_values(left: Any, right: Any) -> Any:
    """
    A custom reducer for strings, bools, and dicts. 
    If parallel nodes return the same key, this safely preserves the newer update.
    """
    if right is None or right == {} or right == []:
        return left
    
    return right

class MessagesState(TypedDict):
    # Persisted message history
    messages: Annotated[List[BaseMessage], add_messages]
    
    # User and rewritten queries
    user_query: Annotated[str, merge_values]
    rag_query: Annotated[str, merge_values]
    tavily_query: Annotated[str, merge_values]
    
    # Internal RAG data
    document_chunks: Annotated[List[Any], merge_values]
    is_relevant: Annotated[bool, merge_values]
    rewrite_count: Annotated[int, merge_values]
    
    # Internal Web Search data
    news_data: Annotated[str, merge_values]
    news_data_formatted: Annotated[str, merge_values]
    
    # Stock info data — live yfinance market data written by stock_node
    stock_info: Annotated[dict, merge_values]
    
    # Ticker routing signal — written by planner, consumed by stock_node
    ticker: Annotated[str, merge_values]
    
    # Final synthesized structured report
    final_report: Annotated[FinalReport, merge_values]
