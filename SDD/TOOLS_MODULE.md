# Tools Module

## Назначение
Модуль добавляет в сервис поддержку инструментов (`tools`) и их привязки к prompt, чтобы модель могла инициировать `tool_call`, а backend безопасно выполнял внешний вызов и возвращал результат модели.

## Состав модуля
- API:
  - `src/api/tools/*` — CRUD реестра инструментов.
  - `src/api/prompts/*` — bind/get инструментов для prompt.
- DB:
  - `src/db/tools/models.py` — `tools`, `prompt_tools`, `tool_call_logs`.
  - `src/db/tools/dals.py` — выборки/замены связей и логов.
- Runtime:
  - `src/modules/tools/orchestrator.py` — цикл `model -> tool -> model`.
  - `src/modules/tools/executor.py` — выполнение HTTP-инструментов с guardrail.
  - `src/modules/tools/validator.py` — базовая валидация аргументов по schema.
  - `src/modules/gpt/tool_calls.py` — вызов OpenAI с `tools`.

## Модель данных

### `tools`
- Реестр доступных инструментов.
- Хранит метаданные (`name`, `description`, `input_schema`) и конфигурацию вызова (`transport`, `method`, `url`, auth/timeouts).
- Поддерживает user-scoped и system-scoped инструменты (`account_id = null`).

### `prompt_tools`
- Связь many-to-many между prompt и tools.
- Поддерживает порядок (`sort_order`) и обязательность (`is_required`).

### `tool_call_logs`
- Аудит каждого вызова инструмента.
- Поля: `status`, `duration_ms`, request/response payload, error text.
- `query_id` может быть `null`, если вызов произошел до успешного сохранения query.

## API

### Tools registry
- `POST /v1/tools/{telegram_id}`
- `GET /v1/tools/{telegram_id}`
- `GET /v1/tools/{telegram_id}/{tool_id}`
- `PUT /v1/tools/{telegram_id}/{tool_id}`
- `DELETE /v1/tools/{telegram_id}/{tool_id}`

Ограничения:
- Создание/изменение/удаление только для owner tools.
- Чужие private tools не выдаются в list/get owner-only сценариях.

### Prompt tool binding
- `PUT /v1/prompts/{telegram_id}/{prompt_id}/tools`
- `GET /v1/prompts/{telegram_id}/{prompt_id}/tools`

Ограничения:
- Привязку меняет только владелец prompt.
- Привязать можно только свои или system tools.

## Выполнение query с tools

В `src/api/queries/actions/prompt_query/post.py`:
1. Загружается prompt.
2. Загружаются активные tools prompt (`_get_active_prompt_tools`).
3. Если tools есть:
   - используется `run_prompt_with_tools`.
   - выполняется цикл до `max_steps` (по умолчанию 5).
4. Если tools нет:
   - используется старый `gpt_handler`.
5. В конце:
   - списание баланса по `cost`,
   - сохранение query,
   - сохранение `tool_call_logs`.

## Guardrails и безопасность
- Запрещены loopback/private host при HTTP tool execution:
  - `localhost`, `127.0.0.1`, private/reserved IP ranges.
- Ограничения:
  - `timeout_sec` (1..60)
  - `max_response_bytes` (1KB..1MB на уровне API; runtime default 256KB)
- Для `transport = mcp` сейчас возвращается controlled error `not implemented`.

## Логика ошибок
- Ошибка валидации аргументов tool -> `validation_error` + контролируемый ответ.
- Ошибка внешнего вызова tool -> `error/timeout` + контролируемый ответ.
- Ошибки фиксируются в `tool_call_logs`.

## Расширение на MCP (следующий этап)
- Добавить `McpToolExecutor`.
- Сохранить единый контракт вызова в orchestrator (`execute_tool`).
- Не менять API bind/list и модель `prompt_tools`.
