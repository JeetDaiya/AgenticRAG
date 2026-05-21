import faiss 
from langchain_community.vectorstores import FAISS
from langchain_core.tools import tool
from agent.core.shared_state import MessagesState
from utils.format_document_list import format_document_list
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    encode_kwargs={"normalize_embeddings": True},
)


vectorstore = FAISS.load_local(
    folder_path='faiss_data',
    index_name='faiss_wells_fargo_index',
    allow_dangerous_deserialization=True,
    embeddings=embeddings
    
)

def retrieve(state: MessagesState):
    """Searches for the chunks of documents which are similary to the input query and returns top 5 of them."""
    query = state.get('rag_query')
    
    docs = vectorstore.max_marginal_relevance_search(query=query, fetch_k=5)
    print(f"   ↳ Retrieved {len(docs)} documents.")
    
    return {"document_chunks": docs}
