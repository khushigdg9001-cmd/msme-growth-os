from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class InventoryItemSnapshot:
    id: UUID
    sku: str
    name: str
    quantity_on_hand: int
    reorder_level: int | None
    unit_cost: Decimal | None
