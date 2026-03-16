# DB and Migrations

## Основные таблицы
- `users`
- `accounts`
- `tokens`
- `user_settings`
- `prompts`
- `queries`
- `scenario`
- `scenario_prompts_relation`

## Важные связи
- `users (1) -> (1) accounts`
- `users (1) -> (1) tokens`
- `users (1) -> (1) user_settings`
- `accounts (1) -> (N) prompts`
- `prompts (1) -> (N) queries`
- `scenario (1) -> (N) scenario_prompts_relation`
- `prompts (1) -> (N) scenario_prompts_relation`

## Кеш query-history
Логика кеша использует поиск "нового похожего запроса" по:
- `prompt_id`
- совпадение текста query
- `time_create > prompt.time_update`

## Индексы для кеша
Введены индексы:
- `ix_queries_prompt_id_time_create` на `(prompt_id, time_create DESC)`
- `ix_queries_prompt_id_query_hash_time_create` на `(prompt_id, md5(query), time_create DESC)`

Это ускоряет проверку кеша без индексации длинного поля ответа (`result`).

## Alembic
- Текущий head в проекте: `9c9f0d5f93b1`.
- Миграция индексов кеша:
  - `alembic/versions/2026_03_16_2300-9c9f0d5f93b1_queries_cache_indexes.py`

## Правила изменений схемы
1. Любое изменение ORM-модели сопровождать Alembic миграцией.
2. Для изменений производительности добавлять проверяемые индексы.
3. Не добавлять индексы на поля с длинными ответами без явного профилирования.
