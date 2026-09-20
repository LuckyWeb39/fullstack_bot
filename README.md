# Telegram Bot on Supabase

Telegram-бот на Supabase Edge Functions. Он сохраняет входящие сообщения и
клиентов в PostgreSQL Supabase, затем отправляет пользователю подтверждение.

## Edge Functions

- `health` — публичная проверка доступности.
- `telegram-webhook` — принимает `POST`-обновления от Telegram, сохраняет их в
  таблицы `clients` и `messages`, затем отвечает пользователю.
- `messages` — публичный `GET`, возвращает сообщения от новых к старым.
- `clients` — публичный `GET`, возвращает клиентов по времени последнего
  сообщения, от новых к старым.

## Деплой

Проект должен быть связан с Supabase через `supabase link`. Деплой всех функций:

```bash
npm run deploy:supabase
```

Публичные endpoints:

```text
https://nwedxcpqqqhnehswwlal.supabase.co/functions/v1/messages
https://nwedxcpqqqhnehswwlal.supabase.co/functions/v1/clients
```

## Secrets

В Supabase Dashboard → Edge Functions → Secrets должны быть добавлены:

- `BOT_TOKEN`
- `TELEGRAM_WEBHOOK_SECRET`

Никогда не добавляй их в Git или README.
