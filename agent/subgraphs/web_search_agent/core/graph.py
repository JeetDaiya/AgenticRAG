from langgraph.graph import StateGraph,START,END
from agent.subgraphs.web_search_agent.nodes.rewrite_for_web import rewrite_for_web
from agent.subgraphs.web_search_agent.nodes.search_web import get_news
from agent.subgraphs.web_search_agent.nodes.web_result_formatter import web_result_formatter
from agent.core.shared_state import MessagesState


web_search_graph_builder = StateGraph(state_schema=MessagesState)

# Adding all the nodes
web_search_graph_builder.add_node("rewrite_for_web", rewrite_for_web)
web_search_graph_builder.add_node("get_news", get_news)
web_search_graph_builder.add_node("web_result_formatted", web_result_formatter)

# Adding the edges

# START -> rewrite_for_web

web_search_graph_builder.add_edge(START, 'rewrite_for_web')

# 1. rewrite_for_web -> get_news

web_search_graph_builder.add_edge('rewrite_for_web', 'get_news')


# 2. get_news -> web_result_formatter

web_search_graph_builder.add_edge('get_news', 'web_result_formatted')

# END -> rewrite_for_web

web_search_graph_builder.add_edge('web_result_formatted', END)



web_search_agent = web_search_graph_builder.compile()
