from typing import Literal
from agent.core.shared_state import MessagesState


def should_rewrite(state: MessagesState) -> Literal["rewrite", "generate"]:
    """Based on the LLM response we decide wether to generate report or rewrite the query"""
    
    if state.get("is_relevant", False):
        return "generate"
    
    return "rewrite"