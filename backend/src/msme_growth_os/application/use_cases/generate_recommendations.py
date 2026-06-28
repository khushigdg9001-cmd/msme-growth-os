from uuid import UUID

from msme_growth_os.ai.graphs.service import RecommendationGraphService
from msme_growth_os.domain.models import RecommendationDraft


class GenerateRecommendationsUseCase:
    def __init__(self, graph_service: RecommendationGraphService | None = None) -> None:
        self._graph_service = graph_service or RecommendationGraphService()

    async def execute(self, business_id: UUID) -> list[RecommendationDraft]:
        return await self._graph_service.run(business_id)
