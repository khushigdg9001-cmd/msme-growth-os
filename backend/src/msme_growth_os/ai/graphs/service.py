from uuid import UUID

from msme_growth_os.ai.graphs import build_recommendation_graph
from msme_growth_os.domain.models import RecommendationDraft


class RecommendationGraphService:
    def __init__(self) -> None:
        self._graph = build_recommendation_graph()

    async def run(self, business_id: UUID) -> list[RecommendationDraft]:
        final_state = await self._graph.ainvoke({"business_id": business_id})
        return final_state.get("recommendations", [])
