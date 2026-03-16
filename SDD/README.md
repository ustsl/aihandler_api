# SDD: System Design Documentation

Этот каталог содержит практичную документацию по backend-сервису `ai_handler`.

## Содержимое
- `LLM_CONTEXT.md`: краткий контекст для LLM-ассистентов и новых участников.
- `ARCHITECTURE.md`: структура проекта, слои и ключевые зависимости.
- `API_WORKFLOWS.md`: основные API-потоки по приложениям (`users`, `prompts`, `queries`, `scenarios`, `analytics`).
- `DB_AND_MIGRATIONS.md`: модель БД, важные связи и индексы (включая кеш query-history).
- `TESTING_GUIDE.md`: как устроены тесты, как запускать и как расширять покрытие.

## Быстрый старт для разработчика
1. Прочитать `ARCHITECTURE.md`.
2. Прочитать `API_WORKFLOWS.md`.
3. Проверить `DB_AND_MIGRATIONS.md` перед изменением моделей.
4. Прогнать `uv run pytest -q` и только после этого вносить изменения.

## Быстрый старт для LLM
1. Прочитать `LLM_CONTEXT.md`.
2. Использовать `API_WORKFLOWS.md` как источник по бизнес-потокам.
3. Проверять инварианты из `DB_AND_MIGRATIONS.md` и `TESTING_GUIDE.md`.
