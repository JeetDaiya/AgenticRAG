from agent.core.model import model
from agent.core.shared_state import MessagesState
from agent.core.pydantic_models.report_model import FinalReport
from utils.format_document_list import format_document_list
import json
from langchain.messages import SystemMessage, HumanMessage
from agent.orchestrator.prompt import GENERATE_SYSTEM_PROMPT
generate_model = model.with_structured_output(schema=FinalReport)

def generate(state : MessagesState):
    """Based on the data collected LLM replies to the user query."""
    
    
    
    docs = state.get('document_chunks', [])
    doc_string = "No RAG Data collected" if len(docs) == 0 else format_document_list(docs)
    
    web_result = state.get('news_data_formatted' , "No Web data requested")
    
    stock_info = state.get('stock_info', {})
    stock_info = "No Stock Information requested" if not stock_info else json.dumps(stock_info, indent=2)
    
    user_query = state.get('user_query')
    
    
    input = f"User Query : {user_query}\n RAG DATA: {doc_string}\n  STOCK INFO: {stock_info}\n WEB RESULT : {web_result}\n "
    
    
    final_report = generate_model.invoke([
        SystemMessage(content=GENERATE_SYSTEM_PROMPT),
        HumanMessage(content=input)
    ])
    
    return {
        "final_report" : final_report
    }
    
