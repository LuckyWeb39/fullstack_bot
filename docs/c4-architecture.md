# C4 architecture

Диаграммы соответствуют текущей FastAPI-версии проекта.

## 1. Context diagram

Показывает систему в целом и её внешние взаимодействия.

```mermaid
C4Context
    title Currency Telegram Bot — System Context

    Person(user, "Пользователь", "Отправляет боту текст с кодом валюты")
    System(bot, "Currency Telegram Bot", "Находит код валюты и возвращает её курс относительно USD")
    System_Ext(telegram, "Telegram", "Передаёт сообщения боту через webhook и принимает ответы")
    System_Ext(frankfurter, "Frankfurter API", "Возвращает актуальные курсы валют")

    Rel(user, telegram, "Отправляет сообщение")
    Rel(telegram, bot, "Передаёт update через webhook")
    Rel(bot, telegram, "Отправляет ответ через Bot API")
    Rel(bot, frankfurter, "Запрашивает курс USD → выбранная валюта")
```

## 2. Container diagram

Приложение разворачивается как один FastAPI-сервис. Внутри него выделены
логические контейнеры, которые отвечают за разные части системы.

```mermaid
C4Container
    title Currency Telegram Bot — Container Diagram

    Person(user, "Пользователь", "Пользователь Telegram")
    System_Ext(telegram, "Telegram", "Telegram Bot API и webhook")
    System_Ext(frankfurter, "Frankfurter API", "API курсов валют")

    System_Boundary(bot, "Currency Telegram Bot") {
        Container(webhook, "Webhook API", "FastAPI", "Принимает Telegram update и возвращает HTTP-ответ")
        Container(core, "Application Core", "Python", "Запускает сценарий поиска кода и получения курса")
        Container(telegram_adapter, "Telegram Adapter", "Python + httpx", "Отправляет сообщения через Telegram Bot API")
        Container(frankfurter_adapter, "Frankfurter Adapter", "Python + httpx", "Получает курс через Frankfurter API")
        Container(config, "Configuration", "Environment variables", "Читает BOT_TOKEN из окружения")
    }

    Rel(user, telegram, "Отправляет сообщение")
    Rel(telegram, webhook, "POST webhook")
    Rel(webhook, core, "Вызывает use case")
    Rel(core, frankfurter_adapter, "Запрашивает курс через port")
    Rel(core, telegram_adapter, "Передаёт готовый ответ через port")
    Rel(frankfurter_adapter, frankfurter, "GET /v1/latest?base=USD&symbols=...")
    Rel(telegram_adapter, telegram, "POST sendMessage")
    Rel(config, webhook, "Предоставляет конфигурацию")
```

## 3. Component diagram

Показывает компоненты внутри FastAPI-приложения и направление зависимостей.

```mermaid
C4Component
    title Currency Telegram Bot — FastAPI Components

    Container_Boundary(api, "FastAPI application") {
        Component(router, "Webhook Router", "app/presentation/webhook.py", "Принимает Telegram update, обрабатывает ошибки и формирует ответ")
        Component(use_case, "GetCurrencyRate", "app/application/use_cases.py", "Находит код валюты и запускает получение курса")
        Component(rate_port, "ExchangeRateProvider", "app/application/ports.py", "Контракт поставщика курсов")
        Component(telegram_port, "TelegramGateway", "app/application/ports.py", "Контракт отправки сообщений")
        Component(rate_adapter, "FrankfurterClient", "app/adapters/frankfurter.py", "Реализация ExchangeRateProvider через httpx")
        Component(telegram_adapter, "TelegramClient", "app/adapters/telegram.py", "Реализация TelegramGateway через httpx")
        Component(domain, "Domain Model and Errors", "app/domain/", "CurrencyRate и доменные ошибки")
        Component(config, "Configuration and Composition", "app/infrastructure/", "Читает BOT_TOKEN и собирает зависимости")
    }

    System_Ext(telegram, "Telegram Bot API", "Внешний Telegram API")
    System_Ext(frankfurter, "Frankfurter API", "Внешний API курсов")

    Rel(router, use_case, "Вызывает execute(text)")
    Rel(router, telegram_port, "Отправляет ответ через контракт")
    Rel(use_case, rate_port, "Запрашивает курс через контракт")
    Rel(use_case, domain, "Использует модель и доменные ошибки")
    Rel(rate_adapter, rate_port, "Реализует контракт")
    Rel(telegram_adapter, telegram_port, "Реализует контракт")
    Rel(rate_adapter, frankfurter, "Запрашивает USD rate")
    Rel(telegram_adapter, telegram, "Отправляет сообщение")
    Rel(config, router, "Собирает и подключает зависимости")
```

