from msme_growth_os.ai.agents.base import BusinessAgent
from msme_growth_os.ai.agents.compliance_agent import ComplianceAgent
from msme_growth_os.ai.agents.crm_agent import CRMAgent
from msme_growth_os.ai.agents.finance_agent import FinanceAgent
from msme_growth_os.ai.agents.inventory_agent import InventoryAgent
from msme_growth_os.ai.agents.supplier_agent import SupplierAgent


def build_default_agents() -> list[BusinessAgent]:
    return [
        InventoryAgent(),
        FinanceAgent(),
        CRMAgent(),
        ComplianceAgent(),
        SupplierAgent(),
    ]
