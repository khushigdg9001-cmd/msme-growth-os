from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from msme_growth_os.ai.agents.inventory_agent import InventoryAgent
from msme_growth_os.application.composition import build_inventory_agent
from msme_growth_os.infrastructure.database.session import get_db_session


async def get_session() -> AsyncIterator[AsyncSession]:
    async for session in get_db_session():
        yield session


def get_inventory_agent(session: AsyncSession = Depends(get_session)) -> InventoryAgent:
    return build_inventory_agent(session)
