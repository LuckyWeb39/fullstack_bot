from typing import Protocol

from app.domain.models import CurrencyRate


class ExchangeRateProvider(Protocol):
    async def get_rate_from_usd(self, currency: str) -> CurrencyRate:
        ...


class TelegramGateway(Protocol):
    async def send_message(self, chat_id: int, text: str) -> None:
        ...

