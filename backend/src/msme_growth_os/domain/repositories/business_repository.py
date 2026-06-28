from abc import ABC, abstractmethod
from uuid import UUID

from msme_growth_os.domain.models import BusinessProfile


class BusinessRepository(ABC):
    @abstractmethod
    async def get_by_id(self, business_id: UUID) -> BusinessProfile | None:
        raise NotImplementedError
