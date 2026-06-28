from typing import Any, TypedDict
from uuid import UUID

from msme_growth_os.ai.agents import AgentOutput
from msme_growth_os.domain.models import RecommendationDraft


class RecommendationGraphState(TypedDict, total=False):
    business_id: UUID
    business_context: dict[str, Any]
    agent_outputs: list[AgentOutput]
    recommendations: list[RecommendationDraft]
