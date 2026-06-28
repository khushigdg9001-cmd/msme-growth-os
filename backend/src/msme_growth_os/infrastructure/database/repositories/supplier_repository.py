from collections import defaultdict
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from msme_growth_os.domain.models import SupplierProfile
from msme_growth_os.infrastructure.database.models import Supplier, SupplierUpdate


class SupplierReadRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_business(self, business_id: UUID) -> list[SupplierProfile]:
        supplier_result = await self._session.execute(
            select(Supplier).where(Supplier.business_id == business_id)
        )
        suppliers = supplier_result.scalars().all()
        supplier_ids = [supplier.id for supplier in suppliers]

        updates_by_supplier_id: dict[UUID, list[str]] = defaultdict(list)
        if supplier_ids:
            update_result = await self._session.execute(
                select(SupplierUpdate).where(SupplierUpdate.supplier_id.in_(supplier_ids))
            )
            for update in update_result.scalars().all():
                updates_by_supplier_id[update.supplier_id].append(update.message)

        return [
            SupplierProfile(
                id=supplier.id,
                name=supplier.name,
                lead_time_days=supplier.lead_time_days,
                updates=updates_by_supplier_id.get(supplier.id, []),
            )
            for supplier in suppliers
        ]
