from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID


@dataclass(frozen=True)
class ComplianceDeadlineRecord:
    id: UUID
    title: str
    category: str
    due_date: date
    status: str


@dataclass(frozen=True)
class ComplianceOrderRecord:
    id: UUID
    status: str
    total_amount: Decimal | None
    external_reference: str | None


@dataclass(frozen=True)
class ComplianceInventoryRecord:
    id: UUID
    sku: str
    name: str
    quantity_on_hand: int
    unit_cost: Decimal | None


@dataclass(frozen=True)
class ComplianceSupplierRecord:
    id: UUID
    name: str
    lead_time_days: int | None
    update_count: int


@dataclass(frozen=True)
class ComplianceCashRecord:
    id: UUID
    available_cash: Decimal
    expected_inflow: Decimal | None
    expected_outflow: Decimal | None
    snapshot_date: date


@dataclass(frozen=True)
class ComplianceDataSnapshot:
    deadlines: list[ComplianceDeadlineRecord]
    orders: list[ComplianceOrderRecord]
    inventory_items: list[ComplianceInventoryRecord]
    suppliers: list[ComplianceSupplierRecord]
    cash_snapshots: list[ComplianceCashRecord]
