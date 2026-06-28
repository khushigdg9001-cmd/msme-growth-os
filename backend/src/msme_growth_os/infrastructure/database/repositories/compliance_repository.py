from collections import Counter
from uuid import UUID

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from msme_growth_os.domain.models import (
    ComplianceCashRecord,
    ComplianceDataSnapshot,
    ComplianceDeadlineRecord,
    ComplianceInventoryRecord,
    ComplianceOrderRecord,
    ComplianceSupplierRecord,
)
from msme_growth_os.infrastructure.database.models import (
    CashSnapshot,
    ComplianceDeadline,
    InventoryItem,
    Order,
    Supplier,
    SupplierUpdate,
)


class ComplianceReadRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_snapshot(self, business_id: UUID) -> ComplianceDataSnapshot:
        deadlines = await self._list_deadlines(business_id)
        orders = await self._list_orders(business_id)
        inventory_items = await self._list_inventory_items(business_id)
        suppliers = await self._list_suppliers(business_id)
        cash_snapshots = await self._list_cash_snapshots(business_id)

        return ComplianceDataSnapshot(
            deadlines=deadlines,
            orders=orders,
            inventory_items=inventory_items,
            suppliers=suppliers,
            cash_snapshots=cash_snapshots,
        )

    async def _list_deadlines(self, business_id: UUID) -> list[ComplianceDeadlineRecord]:
        result = await self._session.execute(
            select(ComplianceDeadline).where(ComplianceDeadline.business_id == business_id)
        )
        return [
            ComplianceDeadlineRecord(
                id=deadline.id,
                title=deadline.title,
                category=deadline.category,
                due_date=deadline.due_date,
                status=deadline.status,
            )
            for deadline in result.scalars().all()
        ]

    async def _list_orders(self, business_id: UUID) -> list[ComplianceOrderRecord]:
        result = await self._session.execute(select(Order).where(Order.business_id == business_id))
        return [
            ComplianceOrderRecord(
                id=order.id,
                status=order.status,
                total_amount=order.total_amount,
                external_reference=order.external_reference,
            )
            for order in result.scalars().all()
        ]

    async def _list_inventory_items(self, business_id: UUID) -> list[ComplianceInventoryRecord]:
        result = await self._session.execute(
            select(InventoryItem).where(InventoryItem.business_id == business_id)
        )
        return [
            ComplianceInventoryRecord(
                id=item.id,
                sku=item.sku,
                name=item.name,
                quantity_on_hand=item.quantity_on_hand,
                unit_cost=item.unit_cost,
            )
            for item in result.scalars().all()
        ]

    async def _list_suppliers(self, business_id: UUID) -> list[ComplianceSupplierRecord]:
        supplier_result = await self._session.execute(
            select(Supplier).where(Supplier.business_id == business_id)
        )
        suppliers = supplier_result.scalars().all()
        supplier_ids = [supplier.id for supplier in suppliers]

        update_counts: Counter[UUID] = Counter()
        if supplier_ids:
            update_result = await self._session.execute(
                select(SupplierUpdate).where(SupplierUpdate.supplier_id.in_(supplier_ids))
            )
            update_counts.update(update.supplier_id for update in update_result.scalars().all())

        return [
            ComplianceSupplierRecord(
                id=supplier.id,
                name=supplier.name,
                lead_time_days=supplier.lead_time_days,
                update_count=update_counts[supplier.id],
            )
            for supplier in suppliers
        ]

    async def _list_cash_snapshots(self, business_id: UUID) -> list[ComplianceCashRecord]:
        result = await self._session.execute(
            select(CashSnapshot)
            .where(CashSnapshot.business_id == business_id)
            .order_by(desc(CashSnapshot.snapshot_date))
        )
        return [
            ComplianceCashRecord(
                id=snapshot.id,
                available_cash=snapshot.available_cash,
                expected_inflow=snapshot.expected_inflow,
                expected_outflow=snapshot.expected_outflow,
                snapshot_date=snapshot.snapshot_date,
            )
            for snapshot in result.scalars().all()
        ]
