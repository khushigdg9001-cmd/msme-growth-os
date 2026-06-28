from fastapi import APIRouter

from msme_growth_os.interfaces.api.v1.schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok")
