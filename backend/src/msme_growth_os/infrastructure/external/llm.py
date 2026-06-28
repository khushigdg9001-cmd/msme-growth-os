from msme_growth_os.core.errors import NotImplementedBusinessLogicError


class LLMClient:
    async def complete(self, prompt: str) -> str:
        raise NotImplementedBusinessLogicError("LLM integration is planned for a later layer.")
