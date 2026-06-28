from fastapi import APIRouter

from msme_growth_os.interfaces.api.v1.routes.inventory import get_inventory
from msme_growth_os.interfaces.api.v1.routes.finance import get_finance
from msme_growth_os.interfaces.api.v1.routes.crm import get_crm
from msme_growth_os.interfaces.api.v1.routes.compliance import get_compliance

from msme_growth_os.services.ai_ceo import generate_ceo_decision
print("AICEO FILE LOADED")
router = APIRouter()


@router.get("/")
async def get_ai_ceo():

    inventory = await get_inventory()

    finance = await get_finance()

    crm = await get_crm()

    compliance = await get_compliance()

    result = generate_ceo_decision(
        inventory,
        finance,
        crm,
        compliance,
    )

    return result