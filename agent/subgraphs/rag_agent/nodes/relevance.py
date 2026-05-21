from agent.core.model import model
from agent.core.shared_state import MessagesState
from agent.core.pydantic_models.relevance_response_model import RelevanceResponse
from utils.format_document_list import format_document_list
from langchain_core.prompts import ChatPromptTemplate
from agent.subgraphs.rag_agent.prompts import RELEVANCE_SYSTEM_PROMPT

def check_relevance(state : MessagesState):
    """LLM looks at retrieved documents and decides whether to proceed for response generation or to go next step."""
    structured_model = model.with_structured_output(schema=RelevanceResponse)
    
    docs = state.get('document_chunks', [])
    
    doc_string = "\n\n".join([doc.page_content for doc in docs])
    query = state.get("rag_query")
    
    
    relevance_prompt = ChatPromptTemplate(
        [
            ("system", RELEVANCE_SYSTEM_PROMPT),
            ("human", "Query : \n{query} \n\n Document Content: \n {doc_string}")
        ]
    )
    
    relevance = relevance_prompt | structured_model
    
    response = relevance.invoke({
        "query" : query,
        "doc_string" : doc_string
    })
    
    is_relevant = False if response.choice.value == "no" else True
    print(f"   ↳ Relevance Decision: {response.choice.value} (is_relevant={is_relevant})")
    
    
    return {
        "is_relevant" : is_relevant
    }
    
    
    
    
    
    
    
    