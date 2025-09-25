import asyncio

from loguru import logger

from src.processing_worker.queue import QueueService


async def main() -> None:

    try:
        logger.info("Start queue!")
        queue_service = QueueService()
        await queue_service.run_async()
    except asyncio.CancelledError as e:
        logger.error(
            f"Cancelled error occured. Gracefully shutdown broker.\nTraceback:\n{e}"
        )
    except Exception as e:
        logger.error(f"Outer exception occured. Trying to restart...\nTraceback:\n{e}")
        # await main()


if __name__ == "__main__":
    asyncio.run(main())
