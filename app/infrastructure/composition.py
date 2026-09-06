from app.adapters.frankfurter import FrankfurterClient
from app.adapters.telegram import TelegramClient
from app.application.use_cases import GetCurrencyRate
from app.infrastructure.config import Settings, get_settings


def create_currency_rate_use_case(settings: Settings) -> GetCurrencyRate:
    rate_provider = FrankfurterClient(settings.frankfurter_url)
    return GetCurrencyRate(rate_provider)


def create_telegram_client(settings: Settings) -> TelegramClient:
    return TelegramClient(settings.bot_token)


def create_dependencies() -> tuple[GetCurrencyRate, TelegramClient]:
    settings = get_settings()
    return create_currency_rate_use_case(settings), create_telegram_client(settings)
