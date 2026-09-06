from fastapi import FastAPI

from app.infrastructure.composition import create_dependencies
from app.presentation.webhook import create_webhook_router


app = FastAPI(title="Currency Telegram Bot")
get_currency_rate, telegram_gateway = create_dependencies()
app.include_router(create_webhook_router(get_currency_rate, telegram_gateway))


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
