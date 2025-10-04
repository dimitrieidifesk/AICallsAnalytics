import asyncio
from concurrent.futures import ProcessPoolExecutor

from loguru import logger
from faststream.rabbit import RabbitBroker

from src.core.config import settings
from src.core.constants import QUEUE_PATH
from src.integrations.broker.schemas import CallSessionProcessingSchema
from src.processing_worker.service.worker import CallSessionProcessingWorker
from src.storage.models.db_helper import db_connector
from src.storage.models.enums import QueueAction


class QueueService:

    def __init__(self) -> None:
        self._broker = RabbitBroker(settings.rabbit.url)

    @staticmethod
    async def handle_queue_message(msg: CallSessionProcessingSchema) -> None:
        try:
            async for session in db_connector.session_getter():
                worker = CallSessionProcessingWorker(session, msg.call_session_id)
                match msg.action:
                    case QueueAction.CREATE:
                        await worker.processing()
                    case QueueAction.UPDATE:
                        await worker.finish_processing()
                    case _:
                        logger.error(f"Unknown action: {msg.action}")
        except Exception as e:
            logger.error(e)

    async def run(self) -> None:
        self._broker.subscriber(queue=QUEUE_PATH)(self.handle_queue_message)
        await self._broker.start()
        try:
            while True:
                await asyncio.sleep(86400)
        except ValueError as e:
            logger.error(f"Value error occured. Continue event loop\nTraceback:\n{e}")
            while True:
                await asyncio.sleep(86400)


async def run_async_queue() -> None:
    queue_service = QueueService()
    await queue_service.run()


def run_sync_queue(index: int) -> None:
    logger.info(f"Start queue {index=}!")
    asyncio.run(run_async_queue())


async def run_in_process_pool(index: int) -> None:
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        await loop.run_in_executor(pool, run_sync_queue, index)
