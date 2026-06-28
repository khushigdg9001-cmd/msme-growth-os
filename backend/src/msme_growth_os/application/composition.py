from sqlalchemy.ext.asyncio import AsyncSession

from msme_growth_os.ai.agents.compliance_agent import ComplianceAgent
from msme_growth_os.ai.agents.crm_agent import CRMAgent
from msme_growth_os.ai.agents.finance_agent import FinanceAgent
from msme_growth_os.ai.agents.inventory_agent import InventoryAgent
from msme_growth_os.ai.agents.supplier_agent import SupplierAgent
from msme_growth_os.ai.decision_engine import MultiAgentOrchestrator
from msme_growth_os.infrastructure.database.repositories.compliance_repository import (
    ComplianceReadRepository,
)
from msme_growth_os.infrastructure.database.repositories.crm_repository import CRMReadRepository
from msme_growth_os.infrastructure.database.repositories.finance_repository import (
    FinanceReadRepository,
)
from msme_growth_os.infrastructure.database.repositories.inventory_repository import (
    InventoryReadRepository,
)
from msme_growth_os.infrastructure.database.repositories.supplier_repository import (
    SupplierReadRepository,
)


def build_inventory_agent(session: AsyncSession) -> InventoryAgent:
    repository = InventoryReadRepository(session)
    return InventoryAgent(repository)


def build_multi_agent_orchestrator(session: AsyncSession) -> MultiAgentOrchestrator:
    return MultiAgentOrchestrator(
        inventory_agent=InventoryAgent(InventoryReadRepository(session)),
        finance_agent=FinanceAgent(FinanceReadRepository(session)),
        crm_agent=CRMAgent(CRMReadRepository(session)),
        supplier_agent=SupplierAgent(SupplierReadRepository(session)),
        compliance_agent=ComplianceAgent(ComplianceReadRepository(session)),
    )
