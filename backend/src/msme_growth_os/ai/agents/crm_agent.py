from datetime import date
from decimal import Decimal
from typing import Protocol
from uuid import UUID

from msme_growth_os.ai.agents.base import AgentInput, AgentOutput, BusinessAgent
from msme_growth_os.core.errors import NotImplementedBusinessLogicError
from msme_growth_os.domain.models import CustomerPurchaseProfile


class CRMRepository(Protocol):
    async def list_customer_purchase_profiles(
        self,
        business_id: UUID,
    ) -> list[CustomerPurchaseProfile]:
        raise NotImplementedError


class CRMAgent(BusinessAgent):
    name = "crm_agent"
    inactivity_threshold_days = 30
    high_value_threshold = Decimal("50000")

    def __init__(self, repository: CRMRepository | None = None) -> None:
        self._repository = repository

    async def analyze(self, agent_input: AgentInput) -> AgentOutput:
        if self._repository is None:
            raise NotImplementedBusinessLogicError(
                "CRM agent requires a CRM repository before analysis."
            )

        customers = await self._repository.list_customer_purchase_profiles(agent_input.business_id)
        as_of_date = self._as_of_date(agent_input)

        repeat_customers = []
        inactive_customers = []
        high_value_customers = []
        purchase_frequency = []
        frequency_insufficient_data = []
        follow_up_recommendations = []

        for customer in customers:
            completed_orders = customer.completed_orders
            total_completed_value = self._total_completed_value(customer)

            if len(completed_orders) > 1:
                repeat_customers.append(self._customer_payload(customer, total_completed_value))

            latest_order = completed_orders[0] if completed_orders else None
            if latest_order is None:
                inactive_payload = self._customer_payload(customer, total_completed_value)
                inactive_payload["reason"] = "no_completed_orders"
                inactive_customers.append(inactive_payload)
                follow_up_recommendations.append(
                    self._follow_up_recommendation(customer, "inactive_customer")
                )
            else:
                days_since_last_order = (as_of_date - latest_order.order_date).days
                if days_since_last_order >= self.inactivity_threshold_days:
                    inactive_payload = self._customer_payload(customer, total_completed_value)
                    inactive_payload["days_since_last_order"] = days_since_last_order
                    inactive_customers.append(inactive_payload)
                    follow_up_recommendations.append(
                        self._follow_up_recommendation(customer, "inactive_customer")
                    )

            if total_completed_value >= self.high_value_threshold:
                high_value_customers.append(self._customer_payload(customer, total_completed_value))

            frequency_signal = self._purchase_frequency_signal(customer)
            if frequency_signal is None:
                frequency_insufficient_data.append(
                    {
                        "customer_id": str(customer.id),
                        "status": "insufficient_data",
                        "reason": "at_least_two_completed_orders_required",
                    }
                )
            else:
                purchase_frequency.append(frequency_signal)

        return AgentOutput(
            agent_name=self.name,
            signals={
                "total_customers": len(customers),
                "repeat_customers": repeat_customers,
                "inactive_customers": inactive_customers,
                "high_value_customers": high_value_customers,
                "customer_purchase_frequency": {
                    "computed": purchase_frequency,
                    "insufficient_data": frequency_insufficient_data,
                },
                "follow_up_recommendations": follow_up_recommendations,
            },
            notes=[],
        )

    def _as_of_date(self, agent_input: AgentInput) -> date:
        context_value = agent_input.context.get("as_of_date")
        if isinstance(context_value, date):
            return context_value
        if isinstance(context_value, str):
            return date.fromisoformat(context_value)
        return date.today()

    def _total_completed_value(self, customer: CustomerPurchaseProfile) -> Decimal:
        return sum(
            (
                order.total_amount
                for order in customer.completed_orders
                if order.total_amount is not None
            ),
            Decimal("0"),
        )

    def _purchase_frequency_signal(
        self,
        customer: CustomerPurchaseProfile,
    ) -> dict[str, object] | None:
        completed_orders = sorted(customer.completed_orders, key=lambda order: order.order_date)
        if len(completed_orders) < 2:
            return None

        first_order_date = completed_orders[0].order_date
        latest_order_date = completed_orders[-1].order_date
        elapsed_days = (latest_order_date - first_order_date).days
        if elapsed_days <= 0:
            return None

        intervals = len(completed_orders) - 1
        average_days_between_orders = elapsed_days / intervals
        return {
            "customer_id": str(customer.id),
            "customer_name": customer.name,
            "completed_order_count": len(completed_orders),
            "average_days_between_orders": round(average_days_between_orders, 2),
            "first_order_date": first_order_date.isoformat(),
            "latest_order_date": latest_order_date.isoformat(),
        }

    def _customer_payload(
        self,
        customer: CustomerPurchaseProfile,
        total_completed_value: Decimal,
    ) -> dict[str, object]:
        latest_order = customer.completed_orders[0] if customer.completed_orders else None
        return {
            "customer_id": str(customer.id),
            "name": customer.name,
            "phone": customer.phone,
            "completed_order_count": len(customer.completed_orders),
            "total_completed_value": str(total_completed_value),
            "latest_order_date": latest_order.order_date.isoformat()
            if latest_order is not None
            else None,
        }

    def _follow_up_recommendation(
        self,
        customer: CustomerPurchaseProfile,
        reason: str,
    ) -> dict[str, str]:
        return {
            "customer_id": str(customer.id),
            "action": "follow_up",
            "reason": reason,
        }
