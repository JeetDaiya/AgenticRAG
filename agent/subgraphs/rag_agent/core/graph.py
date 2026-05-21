from langgraph.graph import START, END, StateGraph
from agent.core.shared_state import MessagesState
from agent.subgraphs.rag_agent.nodes.relevance import check_relevance
from agent.subgraphs.rag_agent.nodes.retrieve import retrieve
from agent.subgraphs.rag_agent.nodes.rewrite import rewrite
from agent.subgraphs.rag_agent.nodes.should_rewrite import should_rewrite

rag_agent_builder = StateGraph(state_schema=MessagesState)

# Adding all the nodes

rag_agent_builder.add_node("retrieve", retrieve)
rag_agent_builder.add_node("rewrite", rewrite)
rag_agent_builder.add_node("relevance", check_relevance)



# Adding the edges

# Start to retrieve

rag_agent_builder.add_edge(START, "retrieve")

# 1. after retrieving check relevance

rag_agent_builder.add_edge("retrieve", "relevance")


# 2. Conditional edge from relevance to rewrite or END

rag_agent_builder.add_conditional_edges(
    "relevance",
    should_rewrite,
    {
        "generate" : END,
        "rewrite" : "rewrite"
    }
)

# 3. Edge from rewrite to retrieve

rag_agent_builder.add_edge(
    "rewrite",
    "retrieve"
)

rag_subgraph = rag_agent_builder.compile()

