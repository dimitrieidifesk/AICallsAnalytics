import asyncio

from loguru import logger
from faststream.rabbit import RabbitBroker

from src.core.config import settings
from src.core.constants import QUEUE_PATH
from src.integrations.broker.schemas import CallSessionProcessingSchema
from src.processing_worker.service.worker import CallSessionProcessingWorker
from src.storage.models.db_helper import db_connector


class QueueService:

    def __init__(self) -> None:
        self._broker = RabbitBroker(settings.rabbit.url)

    @staticmethod
    async def handle_queue_message(msg: CallSessionProcessingSchema) -> None:
        try:
            async for session in db_connector.session_getter():
                worker = CallSessionProcessingWorker(session, msg.call_session_id)
                await worker.processing()
        except Exception as e:
            logger.error(e)

    async def run_async(self) -> None:
        self._broker.subscriber(queue=QUEUE_PATH)(self.handle_queue_message)
        await self._broker.start()
        try:
            while True:
                await asyncio.sleep(86400)
        except ValueError as e:
            logger.error(f"Value error occured. Continue event loop\nTraceback:\n{e}")
            while True:
                await asyncio.sleep(86400)
