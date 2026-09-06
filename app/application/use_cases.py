import re
from decimal import Decimal

from app.application.ports import ExchangeRateProvider
from app.domain.errors import CurrencyCodeNotFoundError, CurrencyNotSupportedError


class GetCurrencyRate:
    _currency_pattern = re.compile(r"(?<![A-Za-z])([A-Za-z]{3})(?![A-Za-z])")

    def __init__(self, rate_provider: ExchangeRateProvider) -> None:
        self._rate_provider = rate_provider

    async def execute(self, text: str) -> str:
        safe_text = text[:1000] if isinstance(text, str) else ""
        match = self._currency_pattern.search(safe_text)
        if not match:
            raise CurrencyCodeNotFoundError

        currency = match.group(1).upper()
        try:
            rate = await self._rate_provider.get_rate_from_usd(currency)
        except ValueError as error:
            raise CurrencyNotSupportedError from error

        return f"1 USD = {self._format_rate(rate.value)} {rate.currency}"

    @staticmethod
    def _format_rate(value: Decimal) -> str:
        return f"{value:.6f}".rstrip("0").rstrip(".") or "0"
