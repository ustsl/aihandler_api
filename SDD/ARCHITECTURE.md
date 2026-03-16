# Architecture

## Технологии
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Alembic
- Pytest

## Слои (приближенно к onion)
- `src/api/*/handlers.py`: HTTP слой, роуты и response-модели.
- `src/api/*/actions/*.py`: бизнес-оркестрация и сценарии use-case.
- `src/db/*/dals.py`: доступ к данным, SQL-запросы.
- `src/db/*/models.py`: ORM-модели.
- `src/modules/gpt/*`: интеграция с AI-провайдером.

## Вход в приложение
- `src/main.py` -> `src/routes.py` -> routers приложений.

## База и сессия
- `src/db/session.py`: `get_db` dependency с `AsyncSession`.
- Для тестов dependency переопределяется в `tests/conftest.py`.

## Поток ошибок
- DAL методы оборачиваются `exception_dal` (`src/db/utils.py`).
- Actions, где нужно, оборачиваются `handle_dal_errors` (`src/api/utils.py`).
- Итог для API: ошибки нормализуются в `HTTPException`.

## Важные точки для рефакторинга в будущем
- Привести user/settings валидацию к единообразному уровню.
- Сузить использование `dict`-ответов с `error` внутри DAL в пользу явных исключений домена.
- Постепенно централизовать auth/permissions в отдельные permission-провайдеры.
