from fastapi import APIRouter

from msme_growth_os.interfaces.api.v1.routes import (
    health,
    recommendations,
    inventory,
    finance,
    crm,
    compliance,
    aiceo,
)

api_v1_router = APIRouter()

api_v1_router.include_router(
    health.router,
    tags=["Health"],
)

api_v1_router.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["Recommendations"],
)

api_v1_router.include_router(
    inventory.router,
    prefix="/inventory",
    tags=["Inventory"],
)

api_v1_router.include_router(
    finance.router,
    prefix="/finance",
    tags=["Finance"],
)

api_v1_router.include_router(
    crm.router,
    prefix="/crm",
    tags=["CRM"],
)

api_v1_router.include_router(
    compliance.router,
    prefix="/compliance",
    tags=["Compliance"],
)
api_v1_router.include_router(
    aiceo.router,
    prefix="/aiceo",
    tags=["AI CEO"],
)