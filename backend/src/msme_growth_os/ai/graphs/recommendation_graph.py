from langgraph.graph import END, StateGraph

from msme_growth_os.ai.graphs.state import RecommendationGraphState


async def collect_context(state: RecommendationGraphState) -> RecommendationGraphState:
    return state


async def run_domain_agents(state: RecommendationGraphState) -> RecommendationGraphState:
    return state


async def rank_recommendations(state: RecommendationGraphState) -> RecommendationGraphState:
    return state


def build_recommendation_graph():
    graph = StateGraph(RecommendationGraphState)
    graph.add_node("collect_context", collect_context)
    graph.add_node("run_domain_agents", run_domain_agents)
    graph.add_node("rank_recommendations", rank_recommendations)
    graph.set_entry_point("collect_context")
    graph.add_edge("collect_context", "run_domain_agents")
    graph.add_edge("run_domain_agents", "rank_recommendations")
    graph.add_edge("rank_recommendations", END)
    return graph.compile()
