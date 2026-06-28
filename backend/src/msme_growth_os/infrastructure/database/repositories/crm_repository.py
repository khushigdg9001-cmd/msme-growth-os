from collections import defaultdict
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from msme_growth_os.domain.models import CustomerOrderRecord, CustomerPurchaseProfile
from msme_growth_os.infrastructure.database.models import Customer, Order


class CRMReadRepository:
    completed_statuses = frozenset({"completed", "paid", "fulfilled"})

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_customer_purchase_profiles(
        self,
        business_id: UUID,
    ) -> list[CustomerPurchaseProfile]:
        customer_result = await self._session.execute(
            select(Customer).where(Customer.business_id == business_id)
        )
        customers = customer_result.scalars().all()

        order_result = await self._session.execute(
            select(Order).where(
                Order.business_id == business_id,
                Order.customer_id.is_not(None),
                Order.status.in_(self.completed_statuses),
            )
        )
        orders_by_customer_id: dict[UUID, list[CustomerOrderRecord]] = defaultdict(list)
        for order in order_result.scalars().all():
            orders_by_customer_id[order.customer_id].append(
                CustomerOrderRecord(
                    id=order.id,
                    status=order.status,
                    total_amount=order.total_amount,
                    order_date=order.created_at.date(),
                )
            )

        return [
            CustomerPurchaseProfile(
                id=customer.id,
                name=customer.name,
                phone=customer.phone,
                completed_orders=sorted(
                    orders_by_customer_id.get(customer.id, []),
                    key=lambda order: order.order_date,
                    reverse=True,
                ),
            )
            for customer in customers
        ]
