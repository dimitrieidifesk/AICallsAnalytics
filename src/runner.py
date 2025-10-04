__all__ = (
    "main_app",
    "main",
)

from src.core.config import settings
from src.core.gunicorn import Application, get_app_options
from src.main import main_app


def main():
    if settings.env == "local":
        import uvicorn

        uvicorn.run("main:main_app", host=settings.run.host, port=settings.run.port, reload=True)
    else:
        Application(
            application=main_app,
            options=get_app_options(
                host=settings.gunicorn.host,
                port=settings.gunicorn.port,
                timeout=settings.gunicorn.timeout,
                workers=settings.gunicorn.workers,
                log_level=settings.logging.log_level,
            ),
        ).run()


if __name__ == "__main__":
    main()
