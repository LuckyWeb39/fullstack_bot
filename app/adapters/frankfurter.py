from decimal import Decimal, InvalidOperation

import httpx

from app.domain.models import CurrencyRate


class FrankfurterClient:
    def __init__(self, base_url: str, timeout: float = 10.0) -> None:
        self._base_url = base_url
        self._timeout = timeout

    async def get_rate_from_usd(self, currency: str) -> CurrencyRate:
        if currency == "USD":
            return CurrencyRate(currency="USD", value=Decimal("1"))

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.get(
                self._base_url,
                params={"base": "USD", "symbols": currency},
            )

        if response.status_code == 404 or response.status_code == 422:
            raise ValueError(f"Unsupported currency: {currency}")
        response.raise_for_status()

        try:
            value = Decimal(str(response.json()["rates"][currency]))
        except (KeyError, InvalidOperation, TypeError) as error:
            raise ValueError("Invalid Frankfurter response") from error

        return CurrencyRate(currency=currency, value=value)

