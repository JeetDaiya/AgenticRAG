from langgraph.graph import StateGraph, START, END
from agent.subgraphs.rag_agent.core.graph import rag_subgraph
from agent.subgraphs.web_search_agent.core.graph import web_search_agent
from agent.orchestrator.nodes.generate import generate
from agent.orchestrator.nodes.planner import planner
from agent.orchestrator.nodes.router import route_from_planner
from agent.core.shared_state import MessagesState
from agent.orchestrator.nodes.stock import stock_node
    


main_agent_builder = StateGraph(state_schema=MessagesState)


# Adding all the nodes

main_agent_builder.add_node("planner", planner)
main_agent_builder.add_node("generate", generate)
main_agent_builder.add_node("rag_agent_node", rag_subgraph)
main_agent_builder.add_node("web_agent_node", web_search_agent)
main_agent_builder.add_node("stock_node", stock_node)



# Adding the edges between nodes

# 1. START -> planner
main_agent_builder.add_edge(START, "planner")

# 2. planner -> router (conditional edge)
# Based on the planner, either go to rag_agent_node, web_agent_node, finance_node or directly generate_node

main_agent_builder.add_conditional_edges(
    "planner",
    route_from_planner,
    {
        "rag_agent_node" : "rag_agent_node",
        "stock_node" : "stock_node",
        "web_agent_node" : "web_agent_node",
        "generate" : "generate"
    }
)

main_agent_builder.add_edge("rag_agent_node", "generate")
main_agent_builder.add_edge("stock_node", "generate")
main_agent_builder.add_edge("web_agent_node", "generate")

main_agent_builder.add_edge("generate", END)



main_agent = main_agent_builder.compile()
