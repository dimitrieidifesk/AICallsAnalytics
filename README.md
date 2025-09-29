# Ai Calls Analytics



## Description
Проект предназначен для анализа телефонных разговоров с применением методов машинного обучения и обработки естественного языка.

📋 Необходимые условия для продакшена:
- Внешняя база данных PostgreSQL.
- Отдельно работающая очередь сообщений (RabbitMQ).
Переменная окружения $REMOTE_PROJECT_DIR должна указывать на удалённый каталог проекта, содержащий .env файл с секретами и конфигурацией.

## Start
Run `docker-compose -f docker-compose.prod.yml up --build` to start the backend.

## Libraries
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [uvicorn](https://www.starlette.io/)
- [alembic](https://alembic.sqlalchemy.org/en/latest/)
- [redis](https://redis.io/)
- [fakeredis](https://pypi.org/project/fakeredis/)
- [gunicorn](https://docs.gunicorn.org/en/latest/index.html)
- [mypy](https://mypy.readthedocs.io/en/stable/index.html)
- [ruff](https://beta.ruff.rs/docs/)
- [asyncpg](https://github.com/MagicStack/asyncpg)
- [pyhumps](https://pyhumps.readthedocs.io/en/latest/)
- [loguru](https://loguru.readthedocs.io/en/stable/)
- [pydantic-settings](https://github.com/pydantic/pydantic-settings)
- [poetry](https://python-poetry.org/)
- [alembic-postgresql-enum](https://pypi.org/project/alembic-postgresql-enum/)
- [aiocache](https://pypi.org/project/aiocache/)
- [aiohttp](https://pypi.org/project/aiohttp/)
- [aiormq](https://pypi.org/project/aiormq/)
- [faststream](https://pypi.org/project/faststream/)


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

### migrations
Директория для миграций базы данных.
- **versions**: Версии миграций.


### logs
Папка с файлами логов.
