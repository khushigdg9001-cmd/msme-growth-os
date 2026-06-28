from typing import Protocol
from uuid import UUID

from msme_growth_os.ai.agents.base import AgentInput, AgentOutput, BusinessAgent
from msme_growth_os.core.errors import NotImplementedBusinessLogicError
from msme_growth_os.domain.models import InventoryItemSnapshot


class InventoryRepository(Protocol):
    async def list_by_business(self, business_id: UUID) -> list[InventoryItemSnapshot]:
        raise NotImplementedError


class InventoryAgent(BusinessAgent):
    name = "inventory_agent"
    overstock_multiplier = 3
    slow_moving_days_threshold = 30
    slow_moving_velocity_threshold = 0

    def __init__(self, repository: InventoryRepository | None = None) -> None:
        self._repository = repository

    async def analyze(self, agent_input: AgentInput) -> AgentOutput:
        if self._repository is None:
            raise NotImplementedBusinessLogicError(
                "Inventory agent requires an inventory repository before analysis."
            )

        items = await self._repository.list_by_business(agent_input.business_id)
        movement_context = self._movement_context(agent_input)

        out_of_stock = []
        low_stock = []
        overstock = []
        slow_moving = []
        recommendations = []
        notes = []

        for item in items:
            item_payload = self._item_payload(item)

            if item.quantity_on_hand <= 0:
                out_of_stock.append(item_payload)
                recommendations.append(
                    self._recommendation(
                        item=item,
                        category="out_of_stock",
                        priority="critical",
                        title=f"Restock {item.name}",
                        reason="Current quantity is zero or below.",
                    )
                )
                continue

            if item.reorder_level is not None and item.quantity_on_hand <= item.reorder_level:
                low_stock.append(item_payload)
                recommendations.append(
                    self._recommendation(
                        item=item,
                        category="low_stock",
                        priority="high",
                        title=f"Review reorder for {item.name}",
                        reason="Current quantity is at or below the configured reorder level.",
                    )
                )

            if self._is_overstocked(item):
                overstock.append(item_payload)
                recommendations.append(
                    self._recommendation(
                        item=item,
                        category="overstock",
                        priority="medium",
                        title=f"Reduce excess stock for {item.name}",
                        reason="Current quantity is significantly above the configured reorder level.",
                    )
                )

            if self._is_slow_moving(item, movement_context):
                slow_moving.append(item_payload)
                recommendations.append(
                    self._recommendation(
                        item=item,
                        category="slow_moving",
                        priority="medium",
                        title=f"Review slow-moving stock for {item.name}",
                        reason="Recent movement data indicates low or no sales activity.",
                    )
                )

        if movement_context is None:
            notes.append("Slow-moving detection skipped because product movement history is unavailable.")

        return AgentOutput(
            agent_name=self.name,
            signals={
                "total_items": len(items),
                "out_of_stock": out_of_stock,
                "low_stock": low_stock,
                "overstock": overstock,
                "slow_moving": slow_moving,
                "recommendations": recommendations,
            },
            notes=notes,
        )

    def _is_overstocked(self, item: InventoryItemSnapshot) -> bool:
        return (
            item.reorder_level is not None
            and item.reorder_level > 0
            and item.quantity_on_hand >= item.reorder_level * self.overstock_multiplier
        )

    def _is_slow_moving(
        self,
        item: InventoryItemSnapshot,
        movement_context: dict[str, dict[str, int | float]] | None,
    ) -> bool:
        if movement_context is None:
            return False

        days_since_last_sale = movement_context.get("days_since_last_sale_by_sku", {}).get(item.sku)
        if (
            days_since_last_sale is not None
            and days_since_last_sale >= self.slow_moving_days_threshold
            and item.quantity_on_hand > 0
        ):
            return True

        sales_velocity = movement_context.get("sales_velocity_by_sku", {}).get(item.sku)
        return (
            sales_velocity is not None
            and sales_velocity <= self.slow_moving_velocity_threshold
            and item.quantity_on_hand > 0
        )

    def _movement_context(
        self,
        agent_input: AgentInput,
    ) -> dict[str, dict[str, int | float]] | None:
        days_since_last_sale = agent_input.context.get("days_since_last_sale_by_sku")
        sales_velocity = agent_input.context.get("sales_velocity_by_sku")

        if not isinstance(days_since_last_sale, dict) and not isinstance(sales_velocity, dict):
            return None

        return {
            "days_since_last_sale_by_sku": days_since_last_sale
            if isinstance(days_since_last_sale, dict)
            else {},
            "sales_velocity_by_sku": sales_velocity if isinstance(sales_velocity, dict) else {},
        }

    def _item_payload(self, item: InventoryItemSnapshot) -> dict[str, object]:
        return {
            "id": str(item.id),
            "sku": item.sku,
            "name": item.name,
            "quantity_on_hand": item.quantity_on_hand,
            "reorder_level": item.reorder_level,
            "unit_cost": str(item.unit_cost) if item.unit_cost is not None else None,
        }

    def _recommendation(
        self,
        item: InventoryItemSnapshot,
        category: str,
        priority: str,
        title: str,
        reason: str,
    ) -> dict[str, object]:
        return {
            "category": category,
            "priority": priority,
            "title": title,
            "reason": reason,
            "item": self._item_payload(item),
        }
