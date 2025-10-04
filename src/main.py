from src.api import router as api_router
from src.factory import create_app


main_app = create_app(
    create_custom_static_urls=True,
)

main_app.include_router(api_router)
