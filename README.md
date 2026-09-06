# Currency Telegram Bot

Минимальный Telegram-бот на FastAPI. Он находит в сообщении трёхбуквенный код
валюты, получает курс через Frankfurter и отвечает, сколько этой валюты стоит
1 USD.

## Локальный запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Переменная `BOT_TOKEN` берётся из `.env`. Проверка приложения:
`http://localhost:8000/health`.

## Деплой на Vercel

1. Импортируй репозиторий в Vercel.
2. В Environment Variables добавь `BOT_TOKEN` со значением токена бота.
3. Нажми Deploy.
4. Проверь `https://YOUR_DOMAIN/health` — должен вернуться `{"status":"ok"}`.
5. Установи Telegram webhook:

```bash
curl "https://api.telegram.org/bot<ТОКЕН>/setWebhook?url=https://YOUR_DOMAIN/webhook"
```

После этого отправь боту, например, `курс EUR`.
