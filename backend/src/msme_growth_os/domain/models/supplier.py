from dataclasses import dataclass, field
from uuid import UUID


@dataclass(frozen=True)
class SupplierProfile:
    id: UUID
    name: str
    lead_time_days: int | None
    updates: list[str] = field(default_factory=list)
