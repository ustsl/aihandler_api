# ТЗ: Поддержка инструментов (Tools) для Prompt в AI Handler

## 1) Цель
Добавить в сервис поддержку инструментов, чтобы при выполнении запроса по `Prompt` модель могла вызывать разрешенные функции, а backend выполнял эти вызовы и возвращал результат модели.

## 2) Уточнение требований
- Да, в OpenAI API инструменты можно передавать явно в поле `tools`.
- Модель не должна вызывать URL напрямую. Модель возвращает `tool_call`, а backend сам выполняет сетевой вызов.
- Привязывать URL напрямую к prompt без реестра инструментов нельзя: это ухудшает безопасность, трассируемость и повторное использование.
- MCP поддержать как отдельный этап через адаптер, а не как единственный MVP-путь.

## 3) Область работ
### В scope (MVP)
- Реестр инструментов (CRUD).
- Связь `Prompt <-> Tool` (many-to-many).
- Выполнение tool-calls в контуре backend.
- Логирование вызовов инструментов.
- Покрытие тестами.

### Out of scope (MVP)
- Полноценная маршрутизация по внешним MCP-серверам.
- UI/админка для инструментов.
- Автогенерация JSON Schema из текста.

## 4) Архитектурные ограничения
- Соблюдать текущий стиль проекта и луковичную архитектуру:
  - `api` -> `actions` -> `dals`/`modules`.
- Интеграцию с OpenAI не разносить по хендлерам: orchestration в отдельном сервисном модуле.
- Новый функционал обязателен к покрытию тестами (unit + integration).

## 5) Доменные сущности и БД
### 5.1 Таблица `tools`
Поля:
- `uuid` (PK, UUID)
- `name` (string, unique, `^[a-zA-Z_][a-zA-Z0-9_]{0,63}$`)
- `description` (string, not null)
- `transport` (enum: `http_json`, `mcp`, default `http_json`)
- `method` (enum: `GET`, `POST`, default `POST`)
- `url` (string, nullable для `mcp`, not null для `http_json`)
- `input_schema` (JSONB, not null; JSON Schema)
- `headers_template` (JSONB, nullable)
- `query_template` (JSONB, nullable)
- `body_template` (JSONB, nullable)
- `auth_type` (enum: `none`, `bearer`, `api_key_query`, default `none`)
- `auth_secret_ref` (string, nullable; ссылка на секрет, не само значение)
- `timeout_sec` (int, default 15, range 1..60)
- `is_active` (bool, default true)
- `account_id` (FK accounts.uuid, nullable; `null` = системный инструмент)
- `time_create`, `time_update`, `is_deleted`, `is_active` (в соответствии с базовыми миксинами проекта)

Индексы:
- unique index на `name`
- index на (`account_id`, `is_active`, `is_deleted`)

### 5.2 Таблица связи `prompt_tools`
Поля:
- `uuid` (PK)
- `prompt_id` (FK prompts.uuid, on delete cascade)
- `tool_id` (FK tools.uuid, on delete cascade)
- `sort_order` (int, default 0)
- `is_required` (bool, default false)
- `time_create`

Ограничения:
- unique (`prompt_id`, `tool_id`)

### 5.3 Таблица аудита `tool_call_logs`
Поля:
- `uuid` (PK)
- `query_id` (FK queries.uuid, nullable если запрос упал до сохранения)
- `prompt_id` (FK prompts.uuid, not null)
- `tool_id` (FK tools.uuid, not null)
- `tool_name` (string)
- `status` (enum: `success`, `error`, `timeout`, `validation_error`)
- `duration_ms` (int)
- `request_payload` (JSONB, sanitized/truncated)
- `response_payload` (JSONB, sanitized/truncated)
- `error_text` (string, nullable)
- `time_create`

## 6) API контракт
### 6.1 Инструменты
- `POST /v1/tools/{telegram_id}`: создать инструмент.
- `GET /v1/tools/{telegram_id}`: список инструментов пользователя + системные.
- `GET /v1/tools/{telegram_id}/{tool_id}`: получить инструмент.
- `PUT /v1/tools/{telegram_id}/{tool_id}`: обновить инструмент.
- `DELETE /v1/tools/{telegram_id}/{tool_id}`: мягкое удаление.

Правила доступа:
- Пользователь может управлять только своими инструментами (`tools.account_id = account.uuid`).
- Системные инструменты (`account_id = null`) доступны на чтение, не на изменение.

### 6.2 Привязка инструментов к Prompt
- `PUT /v1/prompts/{telegram_id}/{prompt_id}/tools`
  - body: `{ "tool_ids": ["uuid1", "uuid2"], "replace": true }`
  - если `replace=true`, текущие связи удаляются и заменяются новыми.
- `GET /v1/prompts/{telegram_id}/{prompt_id}/tools`
  - возвращает список привязанных инструментов.

## 7) Изменения в выполнении запроса (`/v1/queries/...`)
### 7.1 Общий flow
1. Загрузить `Prompt`.
2. Загрузить привязанные к prompt активные tools.
3. Сформировать запрос к OpenAI:
   - `messages` как сейчас,
   - `tools` из реестра (`name`, `description`, `input_schema`).
4. Отправить запрос модели.
5. Если модель вернула `tool_calls`:
   - проверить, что `tool_name` разрешен для этого prompt;
   - валидировать аргументы по `input_schema`;
   - выполнить инструмент через backend executor;
   - добавить в диалог `tool`-сообщение с результатом;
   - повторить вызов модели.
6. Ограничить цикл `tool_calls` (например, max 5 шагов), чтобы избежать бесконечного цикла.
7. Вернуть финальный текст модели, сохранить query и списать баланс как сейчас.

### 7.2 Интерфейсы модулей (слой modules)
- `ToolRegistryService`: получение tool-описаний для prompt.
- `ToolExecutorInterface`: единый контракт выполнения (`execute(tool, args) -> result`).
- `HttpToolExecutor`: реализация для `transport=http_json`.
- `McpToolExecutor` (заглушка на MVP/фаза 2).
- `ToolCallOrchestrator`: цикл `model -> tool -> model`.

## 8) Безопасность
- Запрет выполнения непроверенных URL из prompt/body.
- Разрешены только URL, хранимые в `tools`.
- SSRF-защита: блок private/loopback адресов по умолчанию (`127.0.0.1`, `0.0.0.0`, `localhost`, RFC1918), кроме явно разрешенных конфигурацией.
- Таймаут внешнего вызова обязателен (`timeout_sec`).
- Ограничение размера ответа инструмента (например, 256 KB) + обрезка.
- Секреты не хранить в явном виде в БД; только ссылки (`auth_secret_ref`).
- Логи вызовов не должны содержать токены/секреты.

## 9) MCP стратегия
### Этап 1 (MVP)
- Реализовать только `http_json` tools.
- Поле `transport=mcp` допускается, но исполнение возвращает controlled-error `Not implemented`.

### Этап 2
- Добавить MCP-адаптер:
  - конфиг MCP-сервера,
  - резолв tool по `server/tool_name`,
  - выполнение через MCP client,
  - тот же `ToolExecutorInterface`.

## 10) Тестирование
### Unit tests
- Валидация `input_schema`.
- Резолв инструментов для prompt.
- Проверка ограничений executor (timeout, size limit, SSRF rules).
- Поведение orchestrator: 0 tool-calls, 1 tool-call, несколько tool-calls, превышение лимита.

### Integration tests
- CRUD инструментов и контроль прав доступа.
- Привязка инструментов к prompt.
- Выполнение query с mock OpenAI и mock tool endpoint.
- Негативные сценарии:
  - tool не привязан к prompt,
  - невалидные аргументы,
  - timeout инструмента,
  - ошибка 4xx/5xx у инструмента.

### Regression tests
- Существующие сценарии prompt/query без tools должны работать без изменений.

## 11) Миграции и обратная совместимость
- Создать alembic-миграцию для `tools`, `prompt_tools`, `tool_call_logs`.
- Для существующих prompt ничего не менять: по умолчанию tools отсутствуют.
- API промптов остается совместимым: старые payload продолжают работать.

## 12) Критерии приемки
- Можно создать инструмент, привязать к prompt и увидеть его в prompt-tools.
- При query модель может инициировать tool-call, backend выполняет вызов, модель получает результат и формирует финальный ответ.
- Все ошибки инструментов возвращаются контролируемо, без падения сервиса.
- Баланс и запись query работают как раньше.
- Логи tool-вызовов сохраняются.
- Тесты на новый функционал добавлены и проходят.

## 13) Рекомендуемая декомпозиция задач
1. Миграции + модели + DAL для `tools` и `prompt_tools`.
2. API для CRUD tools и bind/unbind prompt-tools.
3. `ToolExecutorInterface` + `HttpToolExecutor`.
4. Интеграция tool-calls в GPT pipeline.
5. Аудит-лог `tool_call_logs`.
6. Unit/integration/regression тесты.
7. Документация в `README.md` (пример создания tool и запуска query).
