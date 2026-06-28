from typing import Any

from msme_growth_os.ai.agents import AgentInput, AgentOutput, BusinessAgent
from msme_growth_os.ai.decision_engine.ceo_recommendation_engine import CEORecommendationEngine
from msme_growth_os.domain.models import CEORecommendation, SharedBusinessContext


class MultiAgentOrchestrator:
    def __init__(
        self,
        inventory_agent: BusinessAgent,
        finance_agent: BusinessAgent,
        crm_agent: BusinessAgent,
        supplier_agent: BusinessAgent,
        compliance_agent: BusinessAgent,
        ceo_recommendation_engine: CEORecommendationEngine | None = None,
    ) -> None:
        self._agents = [
            inventory_agent,
            finance_agent,
            crm_agent,
            supplier_agent,
            compliance_agent,
        ]
        self._ceo_recommendation_engine = ceo_recommendation_engine or CEORecommendationEngine()

    async def run(self, context: SharedBusinessContext) -> CEORecommendation:
        agent_context = context.to_agent_context()
        agent_outputs: list[AgentOutput] = []

        for agent in self._agents:
            agent_outputs.append(
                await agent.analyze(
                    AgentInput(
                        business_id=context.business_id,
                        context=agent_context,
                    )
                )
            )

        return self._build_final_recommendation(context, agent_outputs)

    def _build_final_recommendation(
        self,
        context: SharedBusinessContext,
        agent_outputs: list[AgentOutput],
    ) -> CEORecommendation:
        agent_output_payloads = [self._agent_output_payload(output) for output in agent_outputs]
        recommended_actions = self._prioritize_actions(
            self._collect_recommended_actions(agent_outputs)
        )
        shared_context = context.with_agent_outputs(
            agent_output_payloads,
            recommended_actions=recommended_actions,
        )
        return self._ceo_recommendation_engine.generate(shared_context)

    def _collect_recommended_actions(
        self,
        agent_outputs: list[AgentOutput],
    ) -> list[dict[str, Any]]:
        actions: list[dict[str, Any]] = []

        for output in agent_outputs:
            for recommendation in output.signals.get("recommendations", []):
                if isinstance(recommendation, dict):
                    actions.append(
                        {
                            "source_agent": output.agent_name,
                            **recommendation,
                        }
                    )

            for follow_up in output.signals.get("follow_up_recommendations", []):
                if isinstance(follow_up, dict):
                    actions.append(
                        {
                            "source_agent": output.agent_name,
                            "category": "customer_follow_up",
                            "priority": "medium",
                            **follow_up,
                        }
                    )

            for urgent_action in output.signals.get("urgent_actions", []):
                if isinstance(urgent_action, dict):
                    actions.append(
                        {
                            "source_agent": output.agent_name,
                            "category": "urgent_compliance_action",
                            "priority": "high",
                            **urgent_action,
                        }
                    )

        return actions

    def _prioritize_actions(self, actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        priority_rank = {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 3,
        }
        return sorted(
            actions,
            key=lambda action: priority_rank.get(
                str(action.get("priority", "low")).lower(),
                priority_rank["low"],
            ),
        )

    def _agent_output_payload(self, output: AgentOutput) -> dict[str, Any]:
        return {
            "agent_name": output.agent_name,
            "signals": output.signals,
            "notes": output.notes,
        }
