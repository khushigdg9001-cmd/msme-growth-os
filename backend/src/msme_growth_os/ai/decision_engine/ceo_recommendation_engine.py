from typing import Any
from uuid import UUID

from msme_growth_os.domain.models import CEORecommendation, SharedBusinessContext


class CEORecommendationEngine:
    priority_rank = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }
    priority_labels = {
        "critical": "Critical",
        "high": "High",
        "medium": "Medium",
        "low": "Low",
    }

    def generate(self, context: SharedBusinessContext) -> CEORecommendation:
        recommended_actions = self._prioritize_actions(context.recommended_actions)
        risks = self._extract_risks(context)
        opportunities = self._extract_opportunities(context)
        top_priorities = recommended_actions[:5]
        business_health_score = self._business_health_score(
            recommended_actions=recommended_actions,
            risks=risks,
        )
        confidence_score = self._confidence_score(context)

        return CEORecommendation(
            business_id=context.business_id,
            executive_summary=self._executive_summary(
                business_health_score=business_health_score,
                recommended_actions=recommended_actions,
                risks=risks,
                opportunities=opportunities,
            ),
            top_priorities=top_priorities,
            risks=risks,
            opportunities=opportunities,
            recommended_actions=recommended_actions,
            confidence_score=confidence_score,
            business_health_score=business_health_score,
            shared_context=context.to_recommendation_context(),
            agent_outputs=list(context.agent_outputs.values()),
            reasoning={
                "agents_used": list(context.agent_outputs.keys()),
                "priority_basis": "agent_recommended_action_priority",
                "risk_basis": "risk_and_insufficient_data_signals_from_agent_outputs",
                "opportunity_basis": "positive_or_actionable_growth_signals_from_agent_outputs",
                "score_basis": "deterministic_scoring_from_agent_outputs_only",
            },
        )

    def _prioritize_actions(self, actions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        prioritized = []
        for action in actions:
            priority = str(action.get("priority", "low")).lower()
            normalized = {
                **action,
                "priority": self.priority_labels.get(priority, "Low"),
            }
            prioritized.append(normalized)

        return sorted(
            prioritized,
            key=lambda action: self.priority_rank.get(
                str(action.get("priority", "Low")).lower(),
                self.priority_rank["low"],
            ),
        )

    def _extract_risks(self, context: SharedBusinessContext) -> list[dict[str, Any]]:
        risks = []
        for domain, insights in context.collected_insights.items():
            for name, signal in insights.items():
                if isinstance(signal, dict):
                    if signal.get("risk") in {"high", "medium"}:
                        risks.append(
                            {
                                "domain": domain,
                                "signal": name,
                                "severity": self.priority_labels.get(str(signal["risk"]), "Medium"),
                                "evidence": signal,
                            }
                        )
                    elif signal.get("status") == "insufficient_data":
                        risks.append(
                            {
                                "domain": domain,
                                "signal": name,
                                "severity": "Medium",
                                "evidence": signal,
                            }
                        )
                elif isinstance(signal, list) and signal:
                    if name in {
                        "out_of_stock",
                        "low_stock",
                        "inactive_customers",
                        "urgent_actions",
                    }:
                        risks.append(
                            {
                                "domain": domain,
                                "signal": name,
                                "severity": self._list_signal_severity(name),
                                "count": len(signal),
                                "evidence": signal,
                            }
                        )
        return risks

    def _extract_opportunities(self, context: SharedBusinessContext) -> list[dict[str, Any]]:
        opportunities = []
        opportunity_signals = {
            "repeat_customers",
            "high_value_customers",
            "customer_purchase_frequency",
            "recommended_supplier",
            "alternative_supplier",
            "price_comparison",
            "delivery_recommendation",
        }
        for domain, insights in context.collected_insights.items():
            for name, signal in insights.items():
                if name not in opportunity_signals:
                    continue
                if self._has_useful_signal(signal):
                    opportunities.append(
                        {
                            "domain": domain,
                            "signal": name,
                            "evidence": signal,
                        }
                    )
        return opportunities

    def _business_health_score(
        self,
        recommended_actions: list[dict[str, Any]],
        risks: list[dict[str, Any]],
    ) -> int:
        score = 100
        for action in recommended_actions:
            priority = str(action.get("priority", "Low")).lower()
            if priority == "critical":
                score -= 20
            elif priority == "high":
                score -= 12
            elif priority == "medium":
                score -= 6

        for risk in risks:
            severity = str(risk.get("severity", "Medium")).lower()
            if severity == "critical":
                score -= 15
            elif severity == "high":
                score -= 10
            elif severity == "medium":
                score -= 5

        return max(0, min(100, score))

    def _confidence_score(self, context: SharedBusinessContext) -> float:
        expected_agents = {
            "inventory_agent",
            "finance_agent",
            "crm_agent",
            "supplier_agent",
            "compliance_agent",
        }
        available_agent_ratio = len(expected_agents.intersection(context.agent_outputs.keys())) / len(
            expected_agents
        )
        insufficient_data_count = self._insufficient_data_count(context)
        confidence = available_agent_ratio - min(0.4, insufficient_data_count * 0.05)
        return round(max(0.0, min(1.0, confidence)), 2)

    def _executive_summary(
        self,
        business_health_score: int,
        recommended_actions: list[dict[str, Any]],
        risks: list[dict[str, Any]],
        opportunities: list[dict[str, Any]],
    ) -> str:
        if recommended_actions:
            first_priority = recommended_actions[0]["priority"]
            return (
                f"Business health score is {business_health_score}/100. "
                f"{len(recommended_actions)} actions require attention, with the top priority marked "
                f"{first_priority}. {len(risks)} risks and {len(opportunities)} opportunities were "
                "identified from agent outputs."
            )
        return (
            f"Business health score is {business_health_score}/100. "
            "No immediate actions were found in current agent outputs."
        )

    def _insufficient_data_count(self, context: SharedBusinessContext) -> int:
        count = 0
        for insights in context.collected_insights.values():
            for signal in insights.values():
                if isinstance(signal, dict):
                    if signal.get("status") == "insufficient_data":
                        count += 1
                    count += sum(
                        1
                        for value in signal.values()
                        if isinstance(value, dict) and value.get("status") == "insufficient_data"
                    )
        return count

    def _has_useful_signal(self, signal: object) -> bool:
        if isinstance(signal, list):
            return bool(signal)
        if isinstance(signal, dict):
            if signal.get("status") == "insufficient_data":
                return False
            computed = signal.get("computed")
            if isinstance(computed, list):
                return bool(computed)
            return bool(signal)
        return False

    def _list_signal_severity(self, signal_name: str) -> str:
        if signal_name in {"out_of_stock", "urgent_actions"}:
            return "Critical"
        if signal_name == "low_stock":
            return "High"
        return "Medium"
