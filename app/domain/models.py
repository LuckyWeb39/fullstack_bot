from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CurrencyRate:
    currency: str
    value: Decimal

