from typing import Any

from fastapi import APIRouter

from app.application.use_cases import GetCurrencyRate
from app.domain.errors import CurrencyCodeNotFoundError, CurrencyNotSupportedError
from app.application.ports import TelegramGateway


def create_webhook_router(
    get_currency_rate: GetCurrencyRate,
    telegram_gateway: TelegramGateway,
) -> APIRouter:
    router = APIRouter()

    @router.post("/webhook")
    async def webhook(update: dict[str, Any]) -> dict[str, bool]:
        message = update.get("message") or update.get("edited_message")
        if not message or not message.get("chat"):
            return {"ok": True}

        try:
            answer = await get_currency_rate.execute(message.get("text", ""))
        except CurrencyCodeNotFoundError:
            answer = "Не нашёл код валюты. Напиши, например: курс EUR"
        except CurrencyNotSupportedError:
            answer = "Не удалось найти такую валюту. Проверь код, например EUR или RUB."
        except Exception:
            answer = "Не удалось получить курс. Попробуй ещё раз чуть позже."

        await telegram_gateway.send_message(message["chat"]["id"], answer)
        return {"ok": True}

    return router

