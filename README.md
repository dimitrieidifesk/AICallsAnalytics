# roi-backend-base-tmp



## Description
Base template for the ROI backend projects.
Has 2 databases (main and test), Redis, and a backend service with a start.sh script that runs migrations and starts the server.
Database connector already developed.
Has 2 modes for starting env=local and env=prod, uvicorn and gunicorn respectively.

## Start
Run `docker-compose up` to start the backend.

## Libraries
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [uvicorn](https://www.starlette.io/)
- [alembic](https://alembic.sqlalchemy.org/en/latest/)
- [redis](https://redis.io/)
- [fakeredis](https://pypi.org/project/fakeredis/)
- [gunicorn](https://docs.gunicorn.org/en/latest/index.html)
- [pytest](https://docs.pytest.org/en/latest/)
- [mypy](https://mypy.readthedocs.io/en/stable/index.html)
- [ruff](https://beta.ruff.rs/docs/)
- [asyncpg](https://github.com/MagicStack/asyncpg)
- [pyhumps](https://pyhumps.readthedocs.io/en/latest/)
- [loguru](https://loguru.readthedocs.io/en/stable/)
- [pydantic-settings](https://github.com/pydantic/pydantic-settings)
- [poetry](https://python-poetry.org/)
- [alembic-postgresql-enum](https://pypi.org/project/alembic-postgresql-enum/)

## Structure

### src
Основная директория с исходным кодом приложения.
- **api**: Реализация API-эндпоинтов.
  - **api_v1**: Эндпоинты версии 1 API.
  - **middlewares**: Миддлвары.
- **core**: Основная логика приложения, включая конфигурацию и утилиты.
  - **gunicorn**: Настройка Gunicorn.
- **integrations**: Интеграции с внешними сервисами.
- **misc**: Прочие вспомогательные модули.
- **services**: Реализация бизнес-логики.
- **storage**: Работа с базами данных.
  - **models** Описание моделей базы данных.
  - **repositories**: Работа с базой данных.

### tests
Модуль для тестирования.
- **fixtures**: Фикстуры для тестов.

### migrations
Директория для миграций базы данных.
- **versions**: Версии миграций.