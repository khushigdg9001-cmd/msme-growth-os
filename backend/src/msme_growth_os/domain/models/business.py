from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class BusinessProfile:
    id: UUID
    name: str
    industry: str | None = None
    city: str | None = None
