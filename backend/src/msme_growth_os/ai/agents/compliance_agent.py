from datetime import date
from typing import Protocol
from uuid import UUID

from msme_growth_os.ai.agents.base import AgentInput, AgentOutput, BusinessAgent
from msme_growth_os.core.errors import NotImplementedBusinessLogicError
from msme_growth_os.domain.models import ComplianceDataSnapshot


class ComplianceRepository(Protocol):
    async def get_snapshot(self, business_id: UUID) -> ComplianceDataSnapshot:
        raise NotImplementedError


class ComplianceAgent(BusinessAgent):
    name = "compliance_agent"
    urgent_deadline_days = 7

    def __init__(self, repository: ComplianceRepository | None = None) -> None:
        self._repository = repository

    async def analyze(self, agent_input: AgentInput) -> AgentOutput:
        if self._repository is None:
            raise NotImplementedBusinessLogicError(
                "Compliance agent requires a compliance repository before analysis."
            )

        snapshot = await self._repository.get_snapshot(agent_input.business_id)
        as_of_date = self._as_of_date(agent_input)

        gst_risk = self._gst_risk(snapshot)
        invoice_risk = self._invoice_risk(snapshot)
        supplier_compliance_risk = self._supplier_compliance_risk(snapshot)
        inventory_documentation_risk = self._inventory_documentation_risk(snapshot)
        financial_reporting_risk = self._financial_reporting_risk(snapshot)
        urgent_actions = self._urgent_actions(snapshot, as_of_date)
        compliance_score = self._compliance_score(
            invoice_risk=invoice_risk,
            supplier_compliance_risk=supplier_compliance_risk,
            inventory_documentation_risk=inventory_documentation_risk,
            financial_reporting_risk=financial_reporting_risk,
            urgent_actions=urgent_actions,
        )

        return AgentOutput(
            agent_name=self.name,
            signals={
                "compliance_status": self._compliance_status(compliance_score, urgent_actions),
                "compliance_score": compliance_score,
                "gst_risk": gst_risk,
                "invoice_risk": invoice_risk,
                "supplier_compliance_risk": supplier_compliance_risk,
                "inventory_documentation_risk": inventory_documentation_risk,
                "financial_reporting_risk": financial_reporting_risk,
                "urgent_actions": urgent_actions,
                "recommendations": self._recommendations(
                    gst_risk=gst_risk,
                    invoice_risk=invoice_risk,
                    supplier_compliance_risk=supplier_compliance_risk,
                    inventory_documentation_risk=inventory_documentation_risk,
                    financial_reporting_risk=financial_reporting_risk,
                    urgent_actions=urgent_actions,
                ),
            },
            notes=[
                "Compliance signals are operational risk indicators, not verified government filings."
            ],
        )

    def _gst_risk(self, snapshot: ComplianceDataSnapshot) -> dict[str, object]:
        gst_deadlines = [
            deadline
            for deadline in snapshot.deadlines
            if deadline.category.lower() == "gst"
        ]
        if not gst_deadlines:
            return {
                "status": None,
                "reason": "GST status cannot be verified because GST filing and return data are not modeled.",
            }

        pending = [
            deadline
            for deadline in gst_deadlines
            if deadline.status.lower() not in {"completed", "filed", "done"}
        ]
        return {
            "status": "risk_detected" if pending else "tracked",
            "pending_deadline_count": len(pending),
            "reason": "Only GST deadline tracking is available; filing status cannot be verified.",
        }

    def _invoice_risk(self, snapshot: ComplianceDataSnapshot) -> dict[str, object]:
        if not snapshot.orders:
            return self._insufficient_data("order_data_required")

        orders_missing_reference = [
            order for order in snapshot.orders if not order.external_reference
        ]
        orders_missing_amount = [
            order for order in snapshot.orders if order.total_amount is None
        ]

        risk_count = len(orders_missing_reference) + len(orders_missing_amount)
        return {
            "risk": "medium" if risk_count else "low",
            "orders_missing_external_reference": len(orders_missing_reference),
            "orders_missing_total_amount": len(orders_missing_amount),
            "reason": "Invoice risk is inferred from missing order reference or amount fields.",
        }

    def _supplier_compliance_risk(self, snapshot: ComplianceDataSnapshot) -> dict[str, object]:
        if not snapshot.suppliers:
            return self._insufficient_data("supplier_data_required")

        suppliers_missing_lead_time = [
            supplier for supplier in snapshot.suppliers if supplier.lead_time_days is None
        ]
        suppliers_without_updates = [
            supplier for supplier in snapshot.suppliers if supplier.update_count == 0
        ]

        risk_count = len(suppliers_missing_lead_time) + len(suppliers_without_updates)
        return {
            "risk": "medium" if risk_count else "low",
            "suppliers_missing_lead_time": len(suppliers_missing_lead_time),
            "suppliers_without_updates": len(suppliers_without_updates),
            "reason": "Supplier compliance is inferred from operational documentation completeness.",
        }

    def _inventory_documentation_risk(self, snapshot: ComplianceDataSnapshot) -> dict[str, object]:
        if not snapshot.inventory_items:
            return self._insufficient_data("inventory_data_required")

        missing_sku = [item for item in snapshot.inventory_items if not item.sku]
        missing_unit_cost = [item for item in snapshot.inventory_items if item.unit_cost is None]
        negative_stock = [item for item in snapshot.inventory_items if item.quantity_on_hand < 0]

        risk_count = len(missing_sku) + len(missing_unit_cost) + len(negative_stock)
        return {
            "risk": "medium" if risk_count else "low",
            "items_missing_sku": len(missing_sku),
            "items_missing_unit_cost": len(missing_unit_cost),
            "items_with_negative_stock": len(negative_stock),
            "reason": "Inventory documentation risk is inferred from SKU, cost, and stock fields.",
        }

    def _financial_reporting_risk(self, snapshot: ComplianceDataSnapshot) -> dict[str, object]:
        if not snapshot.cash_snapshots:
            return self._insufficient_data("cash_snapshot_data_required")

        latest = snapshot.cash_snapshots[0]
        missing_expected_fields = int(latest.expected_inflow is None) + int(
            latest.expected_outflow is None
        )
        return {
            "risk": "medium" if missing_expected_fields else "low",
            "latest_snapshot_date": latest.snapshot_date.isoformat(),
            "missing_expected_inflow": latest.expected_inflow is None,
            "missing_expected_outflow": latest.expected_outflow is None,
            "reason": "Financial reporting completeness is inferred from cash snapshot fields.",
        }

    def _urgent_actions(
        self,
        snapshot: ComplianceDataSnapshot,
        as_of_date: date,
    ) -> list[dict[str, object]]:
        actions = []
        for deadline in snapshot.deadlines:
            status = deadline.status.lower()
            if status in {"completed", "filed", "done"}:
                continue

            days_until_due = (deadline.due_date - as_of_date).days
            if days_until_due < 0:
                actions.append(
                    {
                        "action": "review_overdue_compliance_deadline",
                        "deadline_id": str(deadline.id),
                        "title": deadline.title,
                        "category": deadline.category,
                        "days_overdue": abs(days_until_due),
                    }
                )
            elif days_until_due <= self.urgent_deadline_days:
                actions.append(
                    {
                        "action": "prepare_upcoming_compliance_deadline",
                        "deadline_id": str(deadline.id),
                        "title": deadline.title,
                        "category": deadline.category,
                        "days_until_due": days_until_due,
                    }
                )
        return actions

    def _compliance_score(
        self,
        invoice_risk: dict[str, object],
        supplier_compliance_risk: dict[str, object],
        inventory_documentation_risk: dict[str, object],
        financial_reporting_risk: dict[str, object],
        urgent_actions: list[dict[str, object]],
    ) -> dict[str, object]:
        score = 100
        evaluated_categories = 0
        for signal in [
            invoice_risk,
            supplier_compliance_risk,
            inventory_documentation_risk,
            financial_reporting_risk,
        ]:
            if signal.get("status") == "insufficient_data":
                score -= 10
                continue

            evaluated_categories += 1
            if signal.get("risk") == "medium":
                score -= 15

        if urgent_actions:
            score -= min(30, len(urgent_actions) * 10)

        return {
            "score": max(score, 0),
            "basis": "operational_documentation_completeness",
            "evaluated_categories": evaluated_categories,
            "limitation": "Score does not verify GST filings, tax payments, or statutory submissions.",
        }

    def _compliance_status(
        self,
        compliance_score: dict[str, object],
        urgent_actions: list[dict[str, object]],
    ) -> dict[str, object]:
        if urgent_actions:
            return {
                "status": "attention_required",
                "reason": "One or more compliance deadlines need action.",
            }
        if compliance_score["score"] >= 85:
            return {"status": "operationally_complete", "reason": "No major gaps detected."}
        return {
            "status": "documentation_gaps_detected",
            "reason": "Operational documentation has missing or incomplete fields.",
        }

    def _recommendations(
        self,
        gst_risk: dict[str, object],
        invoice_risk: dict[str, object],
        supplier_compliance_risk: dict[str, object],
        inventory_documentation_risk: dict[str, object],
        financial_reporting_risk: dict[str, object],
        urgent_actions: list[dict[str, object]],
    ) -> list[dict[str, object]]:
        recommendations = []
        if gst_risk.get("status") is None:
            recommendations.append(
                {
                    "category": "gst_risk",
                    "priority": "medium",
                    "action": "add_gst_filing_data_source",
                    "reason": gst_risk["reason"],
                }
            )
        for urgent_action in urgent_actions:
            recommendations.append(
                {
                    "category": "urgent_deadline",
                    "priority": "high",
                    "action": urgent_action["action"],
                    "reason": "Compliance deadline is overdue or due soon.",
                    "evidence": urgent_action,
                }
            )
        for category, signal in [
            ("invoice_risk", invoice_risk),
            ("supplier_compliance_risk", supplier_compliance_risk),
            ("inventory_documentation_risk", inventory_documentation_risk),
            ("financial_reporting_risk", financial_reporting_risk),
        ]:
            if signal.get("risk") == "medium" or signal.get("status") == "insufficient_data":
                recommendations.append(
                    {
                        "category": category,
                        "priority": "medium",
                        "action": "review_operational_documentation",
                        "reason": signal["reason"],
                    }
                )
        return recommendations

    def _as_of_date(self, agent_input: AgentInput) -> date:
        context_value = agent_input.context.get("as_of_date")
        if isinstance(context_value, date):
            return context_value
        if isinstance(context_value, str):
            return date.fromisoformat(context_value)
        return date.today()

    def _insufficient_data(self, reason: str) -> dict[str, str]:
        return {
            "status": "insufficient_data",
            "reason": reason,
        }
