from decimal import Decimal
from typing import Any, Protocol
from uuid import UUID

from msme_growth_os.ai.agents.base import AgentInput, AgentOutput, BusinessAgent
from msme_growth_os.core.errors import NotImplementedBusinessLogicError
from msme_growth_os.domain.models import SupplierProfile


class SupplierRepository(Protocol):
    async def list_by_business(self, business_id: UUID) -> list[SupplierProfile]:
        raise NotImplementedError


class SupplierAgent(BusinessAgent):
    name = "supplier_agent"
    urgent_lead_time_days = 3

    def __init__(self, repository: SupplierRepository | None = None) -> None:
        self._repository = repository

    async def analyze(self, agent_input: AgentInput) -> AgentOutput:
        if self._repository is None:
            raise NotImplementedBusinessLogicError(
                "Supplier agent requires a supplier repository before analysis."
            )

        suppliers = await self._repository.list_by_business(agent_input.business_id)
        context = self._supplier_context(agent_input.context)

        recommended_supplier = self._recommended_supplier(suppliers, context)
        alternative_supplier = self._alternative_supplier(suppliers, recommended_supplier)
        lead_time_risk = self._lead_time_risk(recommended_supplier, context)
        supplier_risk = self._supplier_risk(suppliers, context)
        price_comparison = self._price_comparison(suppliers, context)
        recommended_order_quantity = self._recommended_order_quantity(context)
        estimated_purchase_cost = self._estimated_purchase_cost(
            recommended_supplier,
            recommended_order_quantity,
            context,
        )
        delivery_recommendation = self._delivery_recommendation(
            recommended_supplier,
            lead_time_risk,
            context,
        )

        return AgentOutput(
            agent_name=self.name,
            signals={
                "total_suppliers": len(suppliers),
                "recommended_supplier": recommended_supplier,
                "alternative_supplier": alternative_supplier,
                "supplier_risk": supplier_risk,
                "lead_time_risk": lead_time_risk,
                "price_comparison": price_comparison,
                "recommended_order_quantity": recommended_order_quantity,
                "estimated_purchase_cost": estimated_purchase_cost,
                "delivery_recommendation": delivery_recommendation,
            },
            notes=[],
        )

    def _recommended_supplier(
        self,
        suppliers: list[SupplierProfile],
        context: dict[str, Any],
    ) -> dict[str, object]:
        if not suppliers:
            return self._insufficient_data("no_suppliers_available")

        candidates = [supplier for supplier in suppliers if supplier.lead_time_days is not None]
        if not candidates:
            return self._insufficient_data("supplier_lead_time_required")

        urgency = context.get("inventory_urgency")
        reliability_by_supplier_id = context.get("reliability_by_supplier_id")
        price_by_supplier_id = context.get("price_by_supplier_id")

        ranked = sorted(
            candidates,
            key=lambda supplier: (
                self._lead_time_score(supplier, urgency),
                -self._reliability_score(supplier, reliability_by_supplier_id),
                self._price_score(supplier, price_by_supplier_id),
            ),
        )
        supplier = ranked[0]
        reasons = ["lead_time_considered"]
        if isinstance(reliability_by_supplier_id, dict):
            reasons.append("reliability_considered")
        if isinstance(price_by_supplier_id, dict):
            reasons.append("price_considered_after_lead_time_and_reliability")

        return {
            "supplier": self._supplier_payload(supplier),
            "status": "recommended",
            "reasoning": reasons,
        }

    def _alternative_supplier(
        self,
        suppliers: list[SupplierProfile],
        recommended_supplier: dict[str, object],
    ) -> dict[str, object]:
        if recommended_supplier.get("status") == "insufficient_data":
            return self._insufficient_data("recommended_supplier_unavailable")

        recommended_id = recommended_supplier["supplier"]["id"]
        alternatives = [
            supplier for supplier in suppliers if str(supplier.id) != recommended_id
        ]
        alternatives_with_lead_time = [
            supplier for supplier in alternatives if supplier.lead_time_days is not None
        ]
        if not alternatives_with_lead_time:
            return self._insufficient_data("no_alternative_supplier_with_lead_time")

        supplier = sorted(alternatives_with_lead_time, key=lambda item: item.lead_time_days or 0)[0]
        return {
            "supplier": self._supplier_payload(supplier),
            "status": "available",
            "reason": "next_shortest_known_lead_time",
        }

    def _supplier_risk(
        self,
        suppliers: list[SupplierProfile],
        context: dict[str, Any],
    ) -> dict[str, object]:
        if not suppliers:
            return self._insufficient_data("no_suppliers_available")

        reliability_by_supplier_id = context.get("reliability_by_supplier_id")
        if not isinstance(reliability_by_supplier_id, dict):
            return self._insufficient_data("supplier_reliability_data_required")

        risks = []
        for supplier in suppliers:
            reliability = reliability_by_supplier_id.get(str(supplier.id))
            if reliability is None:
                risks.append(
                    {
                        "supplier_id": str(supplier.id),
                        "supplier_name": supplier.name,
                        "status": "insufficient_data",
                        "reason": "missing_reliability_score",
                    }
                )
            elif Decimal(str(reliability)) < Decimal("0.70"):
                risks.append(
                    {
                        "supplier_id": str(supplier.id),
                        "supplier_name": supplier.name,
                        "risk": "low_reliability",
                        "reliability_score": str(reliability),
                    }
                )

        return {"risks": risks}

    def _lead_time_risk(
        self,
        recommended_supplier: dict[str, object],
        context: dict[str, Any],
    ) -> dict[str, object]:
        if recommended_supplier.get("status") == "insufficient_data":
            return self._insufficient_data("recommended_supplier_unavailable")

        supplier = recommended_supplier["supplier"]
        lead_time_days = supplier["lead_time_days"]
        if lead_time_days is None:
            return self._insufficient_data("supplier_lead_time_required")

        inventory_urgency = context.get("inventory_urgency")
        max_acceptable_lead_time_days = (
            self.urgent_lead_time_days if inventory_urgency == "urgent" else None
        )
        if max_acceptable_lead_time_days is None:
            return {
                "risk": "unknown",
                "reason": "inventory_urgency_required",
                "lead_time_days": lead_time_days,
            }

        if lead_time_days > max_acceptable_lead_time_days:
            return {
                "risk": "high",
                "lead_time_days": lead_time_days,
                "max_acceptable_lead_time_days": max_acceptable_lead_time_days,
            }

        return {
            "risk": "low",
            "lead_time_days": lead_time_days,
            "max_acceptable_lead_time_days": max_acceptable_lead_time_days,
        }

    def _price_comparison(
        self,
        suppliers: list[SupplierProfile],
        context: dict[str, Any],
    ) -> dict[str, object]:
        price_by_supplier_id = context.get("price_by_supplier_id")
        if not isinstance(price_by_supplier_id, dict):
            return self._insufficient_data("supplier_price_data_required")

        prices = []
        for supplier in suppliers:
            price = price_by_supplier_id.get(str(supplier.id))
            if price is not None:
                prices.append(
                    {
                        "supplier_id": str(supplier.id),
                        "supplier_name": supplier.name,
                        "unit_price": str(Decimal(str(price))),
                    }
                )

        if len(prices) < 2:
            return self._insufficient_data("at_least_two_supplier_prices_required")

        return {"prices": prices}

    def _recommended_order_quantity(self, context: dict[str, Any]) -> dict[str, object]:
        current_stock = context.get("current_stock")
        reorder_level = context.get("reorder_level")
        expected_customer_demand = context.get("expected_customer_demand")

        if current_stock is None or reorder_level is None:
            return self._insufficient_data("current_stock_and_reorder_level_required")

        demand_buffer = Decimal(str(expected_customer_demand or 0))
        target_stock = Decimal(str(reorder_level)) + demand_buffer
        quantity = target_stock - Decimal(str(current_stock))
        if quantity <= 0:
            quantity = Decimal("0")

        return {
            "quantity": int(quantity),
            "reasoning": {
                "current_stock": str(current_stock),
                "reorder_level": str(reorder_level),
                "expected_customer_demand": str(expected_customer_demand)
                if expected_customer_demand is not None
                else None,
            },
        }

    def _estimated_purchase_cost(
        self,
        recommended_supplier: dict[str, object],
        recommended_order_quantity: dict[str, object],
        context: dict[str, Any],
    ) -> dict[str, object]:
        if recommended_supplier.get("status") == "insufficient_data":
            return self._insufficient_data("recommended_supplier_unavailable")
        if "quantity" not in recommended_order_quantity:
            return self._insufficient_data("recommended_order_quantity_required")

        price_by_supplier_id = context.get("price_by_supplier_id")
        if not isinstance(price_by_supplier_id, dict):
            return self._insufficient_data("supplier_price_data_required")

        supplier_id = recommended_supplier["supplier"]["id"]
        unit_price = price_by_supplier_id.get(supplier_id)
        if unit_price is None:
            return self._insufficient_data("recommended_supplier_price_required")

        quantity = Decimal(str(recommended_order_quantity["quantity"]))
        estimated_cost = quantity * Decimal(str(unit_price))
        available_cash = context.get("available_cash")
        cash_status = "insufficient_data"
        if available_cash is not None:
            cash_status = (
                "within_available_cash"
                if estimated_cost <= Decimal(str(available_cash))
                else "exceeds_available_cash"
            )

        return {
            "quantity": int(quantity),
            "unit_price": str(Decimal(str(unit_price))),
            "estimated_cost": str(estimated_cost),
            "available_cash": str(available_cash) if available_cash is not None else None,
            "cash_status": cash_status,
        }

    def _delivery_recommendation(
        self,
        recommended_supplier: dict[str, object],
        lead_time_risk: dict[str, object],
        context: dict[str, Any],
    ) -> dict[str, object]:
        if recommended_supplier.get("status") == "insufficient_data":
            return self._insufficient_data("recommended_supplier_unavailable")

        if lead_time_risk.get("risk") == "high":
            return {
                "action": "expedite_or_use_alternative",
                "reason": "lead_time_risk_high",
                "supplier_id": recommended_supplier["supplier"]["id"],
            }

        if context.get("inventory_urgency") == "urgent":
            return {
                "action": "place_order_immediately",
                "reason": "urgent_inventory_need",
                "supplier_id": recommended_supplier["supplier"]["id"],
            }

        return {
            "action": "schedule_standard_delivery",
            "reason": "lead_time_acceptable_or_urgency_unknown",
            "supplier_id": recommended_supplier["supplier"]["id"],
        }

    def _supplier_context(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "inventory_urgency": context.get("inventory_urgency"),
            "current_stock": context.get("current_stock"),
            "reorder_level": context.get("reorder_level"),
            "expected_customer_demand": context.get("expected_customer_demand"),
            "available_cash": context.get("available_cash"),
            "price_by_supplier_id": context.get("price_by_supplier_id"),
            "reliability_by_supplier_id": context.get("reliability_by_supplier_id"),
        }

    def _lead_time_score(self, supplier: SupplierProfile, urgency: object) -> int:
        lead_time_days = supplier.lead_time_days or 999999
        if urgency == "urgent":
            return lead_time_days
        return lead_time_days

    def _reliability_score(
        self,
        supplier: SupplierProfile,
        reliability_by_supplier_id: object,
    ) -> Decimal:
        if not isinstance(reliability_by_supplier_id, dict):
            return Decimal("0")
        return Decimal(str(reliability_by_supplier_id.get(str(supplier.id), 0)))

    def _price_score(self, supplier: SupplierProfile, price_by_supplier_id: object) -> Decimal:
        if not isinstance(price_by_supplier_id, dict):
            return Decimal("0")
        price = price_by_supplier_id.get(str(supplier.id))
        if price is None:
            return Decimal("999999999")
        return Decimal(str(price))

    def _supplier_payload(self, supplier: SupplierProfile) -> dict[str, object]:
        return {
            "id": str(supplier.id),
            "name": supplier.name,
            "lead_time_days": supplier.lead_time_days,
        }

    def _insufficient_data(self, reason: str) -> dict[str, str]:
        return {
            "status": "insufficient_data",
            "reason": reason,
        }
