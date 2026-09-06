import httpx


class TelegramClient:
    def __init__(self, bot_token: str, timeout: float = 10.0) -> None:
        self._url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        self._timeout = timeout

    async def send_message(self, chat_id: int, text: str) -> None:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(
                self._url,
                json={"chat_id": chat_id, "text": text},
            )
        response.raise_for_status()
