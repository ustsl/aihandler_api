# API Workflows

## 1) Users

### Создание пользователя
`POST /v1/users/`
- Создает `users` + связанные `accounts`, `tokens`, `user_settings`.
- Доступ по `SERVICE_TOKEN`.

### Баланс
`PUT /v1/users/{telegram_id}/balance`
- Изменяет баланс аккаунта пользователя.
- Используется для пополнения/списания.

### Настройки
`PUT /v1/users/{telegram_id}/settings`
`PUT /v1/users/{telegram_id}/prompt` (deprecated alias)
- Обновляет `language`/`prompt_id` в `user_settings`.

### Токен
`PUT /v1/users/{telegram_id}/token`
- Регенерирует user token.

## 2) Prompts

### Создание
`POST /v1/prompts/{telegram_id}`
- Привязывает prompt к account владельца.

### Список
`GET /v1/prompts/{telegram_id}?only_yours=true|false`
- `only_yours=true`: только свои.
- `only_yours=false`: свои + открытые (`is_open=true`) чужие.

### Детали
`GET /v1/prompts/{telegram_id}/{prompt_id}`
- Открытый prompt доступен всем.
- Приватный (`is_open=false`) только владельцу.

### Обновление/удаление
`PUT/DELETE /v1/prompts/{telegram_id}/{prompt_id}`
- Только владелец.
- Удаление мягкое (`is_deleted=true`).

## 3) Queries

### Выполнение запроса
`POST /v1/queries/{telegram_id}`
- Загружает prompt.
- Проверяет баланс.
- При необходимости срезает историю (`context_story_window`).
- Проверяет кеш истории для похожего запроса.
- При кеш-хите возвращает сохраненный ответ без списания.
- При кеше-мисс вызывает AI, сохраняет query, списывает стоимость.

### История по prompt
`GET /v1/queries/{telegram_id}/{prompt_id}`
- Возвращает персональную историю запросов по prompt.

## 4) Scenarios

### Создание и обновление
`POST /v1/scenarios/{telegram_id}`
`PUT /v1/scenarios/{telegram_id}/{scenario_id}`
- Сценарий связывается с владельцем.
- В обновлении можно задавать список prompt-этапов (`order`, `independent`).

### Запуск сценария
`POST /v1/queries/{telegram_id}/scenario`
- Проходит prompt-этапы по порядку.
- Если `independent=false`, на следующий шаг передается предыдущий результат.

## 5) Analytics

### Общий список запросов
`GET /v1/analytics/queries`
- Сервисная аналитика, доступ по `SERVICE_TOKEN`.
