from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class CustomerOrderRecord:
    id: UUID
    status: str
    total_amount: Decimal | None
    order_date: date


@dataclass(frozen=True)
class CustomerPurchaseProfile:
    id: UUID
    name: str
    phone: str | None
    completed_orders: list[CustomerOrderRecord] = field(default_factory=list)
