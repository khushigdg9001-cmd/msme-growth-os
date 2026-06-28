from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from msme_growth_os.domain.models import InventoryItemSnapshot
from msme_growth_os.infrastructure.database.models import InventoryItem


class InventoryReadRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_by_business(self, business_id: UUID) -> list[InventoryItemSnapshot]:
        result = await self._session.execute(
            select(InventoryItem).where(InventoryItem.business_id == business_id)
        )
        items = result.scalars().all()
        return [
            InventoryItemSnapshot(
                id=item.id,
                sku=item.sku,
                name=item.name,
                quantity_on_hand=item.quantity_on_hand,
                reorder_level=item.reorder_level,
                unit_cost=item.unit_cost,
            )
            for item in items
        ]
