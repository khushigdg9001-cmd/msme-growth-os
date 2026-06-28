from msme_growth_os.core.errors import NotImplementedBusinessLogicError


class WhatsAppBusinessClient:
    async def send_message(self, phone_number: str, message: str) -> None:
        raise NotImplementedBusinessLogicError("WhatsApp integration is planned for a later layer.")
