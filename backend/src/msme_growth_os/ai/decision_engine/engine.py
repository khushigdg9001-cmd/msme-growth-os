from msme_growth_os.ai.agents import AgentOutput
from msme_growth_os.core.errors import NotImplementedBusinessLogicError
from msme_growth_os.domain.models import RecommendationDraft


class DecisionEngine:
    async def rank_actions(self, agent_outputs: list[AgentOutput]) -> list[RecommendationDraft]:
        raise NotImplementedBusinessLogicError("Decision ranking is planned for a later layer.")
