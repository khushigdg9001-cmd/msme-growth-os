from decimal import Decimal
from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from msme_growth_os.domain.models import CashSnapshotRecord, ReceivableRecord
from msme_growth_os.infrastructure.database.models import CashSnapshot, Order


class FinanceReadRepository:
    receivable_statuses = frozenset({"pending_payment", "unpaid", "partially_paid", "overdue"})

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_cash_snapshots(self, business_id: UUID) -> list[CashSnapshotRecord]:
        result = await self._session.execute(
            select(CashSnapshot)
            .where(CashSnapshot.business_id == business_id)
            .order_by(desc(CashSnapshot.snapshot_date))
        )
        snapshots = result.scalars().all()
        return [
            CashSnapshotRecord(
                id=snapshot.id,
                available_cash=snapshot.available_cash,
                expected_inflow=snapshot.expected_inflow,
                expected_outflow=snapshot.expected_outflow,
                snapshot_date=snapshot.snapshot_date,
            )
            for snapshot in snapshots
        ]

    async def list_outstanding_receivables(self, business_id: UUID) -> list[ReceivableRecord]:
        result = await self._session.execute(
            select(Order).where(
                Order.business_id == business_id,
                Order.status.in_(self.receivable_statuses),
                Order.total_amount.is_not(None),
            )
        )
        orders = result.scalars().all()
        return [
            ReceivableRecord(
                id=order.id,
                status=order.status,
                total_amount=order.total_amount or Decimal("0"),
            )
            for order in orders
        ]
