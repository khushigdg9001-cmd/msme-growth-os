from dataclasses import dataclass, field
from datetime import date
from typing import Any
from uuid import UUID


@dataclass(frozen=True)
class SharedBusinessContext:
    business_id: UUID
    business_name: str | None = None
    as_of_date: date | None = None
    inventory_status: dict[str, Any] = field(default_factory=dict)
    financial_constraints: dict[str, Any] = field(default_factory=dict)
    customer_demand: dict[str, Any] = field(default_factory=dict)
    supplier_preferences: dict[str, Any] = field(default_factory=dict)
    compliance_context: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    agent_outputs: dict[str, dict[str, Any]] = field(default_factory=dict)
    inventory_insights: dict[str, Any] = field(default_factory=dict)
    finance_insights: dict[str, Any] = field(default_factory=dict)
    crm_insights: dict[str, Any] = field(default_factory=dict)
    supplier_insights: dict[str, Any] = field(default_factory=dict)
    compliance_insights: dict[str, Any] = field(default_factory=dict)
    overall_business_health: dict[str, Any] = field(default_factory=dict)
    collected_insights: dict[str, dict[str, Any]] = field(default_factory=dict)
    recommended_actions: list[dict[str, Any]] = field(default_factory=list)

    def to_agent_context(self) -> dict[str, Any]:
        context: dict[str, Any] = {
            **self.inventory_status,
            **self.financial_constraints,
            **self.customer_demand,
            **self.supplier_preferences,
            **self.compliance_context,
            **self.metadata,
        }
        if self.business_name is not None:
            context["business_name"] = self.business_name
        if self.as_of_date is not None:
            context["as_of_date"] = self.as_of_date.isoformat()
        return context

    def with_agent_outputs(
        self,
        agent_outputs: list[dict[str, Any]],
        recommended_actions: list[dict[str, Any]] | None = None,
    ) -> "SharedBusinessContext":
        collected_outputs = {
            output["agent_name"]: output
            for output in agent_outputs
            if isinstance(output.get("agent_name"), str)
        }
        inventory_insights = self._signals_for(collected_outputs, "inventory_agent")
        finance_insights = self._signals_for(collected_outputs, "finance_agent")
        crm_insights = self._signals_for(collected_outputs, "crm_agent")
        supplier_insights = self._signals_for(collected_outputs, "supplier_agent")
        compliance_insights = self._signals_for(collected_outputs, "compliance_agent")
        actions = recommended_actions or []

        return SharedBusinessContext(
            business_id=self.business_id,
            business_name=self.business_name,
            as_of_date=self.as_of_date,
            inventory_status=self.inventory_status,
            financial_constraints=self.financial_constraints,
            customer_demand=self.customer_demand,
            supplier_preferences=self.supplier_preferences,
            compliance_context=self.compliance_context,
            metadata=self.metadata,
            agent_outputs=collected_outputs,
            inventory_insights=inventory_insights,
            finance_insights=finance_insights,
            crm_insights=crm_insights,
            supplier_insights=supplier_insights,
            compliance_insights=compliance_insights,
            overall_business_health=self._overall_business_health(
                collected_outputs=collected_outputs,
                recommended_actions=actions,
            ),
            collected_insights={
                "inventory": inventory_insights,
                "finance": finance_insights,
                "crm": crm_insights,
                "supplier": supplier_insights,
                "compliance": compliance_insights,
            },
            recommended_actions=actions,
        )

    def to_recommendation_context(self) -> dict[str, Any]:
        return {
            "business_id": str(self.business_id),
            "business_name": self.business_name,
            "as_of_date": self.as_of_date.isoformat() if self.as_of_date is not None else None,
            "inventory_insights": self.inventory_insights,
            "finance_insights": self.finance_insights,
            "crm_insights": self.crm_insights,
            "supplier_insights": self.supplier_insights,
            "compliance_insights": self.compliance_insights,
            "overall_business_health": self.overall_business_health,
            "agent_outputs": self.agent_outputs,
            "collected_insights": self.collected_insights,
            "recommended_actions": self.recommended_actions,
        }

    def _signals_for(
        self,
        collected_outputs: dict[str, dict[str, Any]],
        agent_name: str,
    ) -> dict[str, Any]:
        output = collected_outputs.get(agent_name, {})
        signals = output.get("signals", {})
        return signals if isinstance(signals, dict) else {}

    def _overall_business_health(
        self,
        collected_outputs: dict[str, dict[str, Any]],
        recommended_actions: list[dict[str, Any]],
    ) -> dict[str, Any]:
        critical_actions = self._count_actions_by_priority(recommended_actions, "critical")
        high_actions = self._count_actions_by_priority(recommended_actions, "high")
        medium_actions = self._count_actions_by_priority(recommended_actions, "medium")
        high_risk_signals = self._count_risk_signals(collected_outputs, "high")

        if critical_actions:
            status = "critical"
        elif high_actions or high_risk_signals:
            status = "attention_required"
        elif medium_actions:
            status = "watch"
        else:
            status = "stable"

        return {
            "status": status,
            "critical_action_count": critical_actions,
            "high_action_count": high_actions,
            "medium_action_count": medium_actions,
            "high_risk_signal_count": high_risk_signals,
            "basis": "agent_outputs_and_recommended_action_priorities",
        }

    def _count_actions_by_priority(
        self,
        recommended_actions: list[dict[str, Any]],
        priority: str,
    ) -> int:
        return sum(
            1
            for action in recommended_actions
            if str(action.get("priority", "")).lower() == priority
        )

    def _count_risk_signals(
        self,
        collected_outputs: dict[str, dict[str, Any]],
        risk: str,
    ) -> int:
        count = 0
        for output in collected_outputs.values():
            signals = output.get("signals", {})
            if not isinstance(signals, dict):
                continue
            for signal in signals.values():
                if isinstance(signal, dict) and signal.get("risk") == risk:
                    count += 1
        return count


@dataclass(frozen=True)
class CEORecommendation:
    business_id: UUID
    executive_summary: str
    top_priorities: list[dict[str, Any]]
    risks: list[dict[str, Any]]
    opportunities: list[dict[str, Any]]
    recommended_actions: list[dict[str, Any]]
    confidence_score: float
    business_health_score: int
    shared_context: dict[str, Any]
    agent_outputs: list[dict[str, Any]]
    reasoning: dict[str, Any]


AICEORecommendation = CEORecommendation
