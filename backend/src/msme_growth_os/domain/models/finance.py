from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class CashSnapshotRecord:
    id: UUID
    available_cash: Decimal
    expected_inflow: Decimal | None
    expected_outflow: Decimal | None
    snapshot_date: date


@dataclass(frozen=True)
class ReceivableRecord:
    id: UUID
    status: str
    total_amount: Decimal
