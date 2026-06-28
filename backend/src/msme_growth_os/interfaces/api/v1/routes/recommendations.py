from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from msme_growth_os.application.composition import build_multi_agent_orchestrator
from msme_growth_os.domain.models import SharedBusinessContext
from msme_growth_os.interfaces.api.dependencies import get_session

router = APIRouter()


@router.post("/{business_id}")
async def request_recommendations(
    business_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    orchestrator = build_multi_agent_orchestrator(session)

    context = SharedBusinessContext(
        business_id=business_id,
    )

    recommendation = await orchestrator.run(context)

    return recommendation