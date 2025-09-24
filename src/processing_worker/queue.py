import asyncio

from loguru import logger
from faststream.rabbit import RabbitBroker

from src.core.config import settings
from src.core.constants import QUEUE_PATH
from src.integrations.broker.schemas import CallSessionProcessingSchema


class QueueService:

    def __init__(self) -> None:
        self._broker = RabbitBroker(settings.rabbit.url)

    async def handle_queue_message(self, msg: CallSessionProcessingSchema) -> None:
        ...

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


async def run_async_queue() -> None:
    queue_service = QueueService()
    await queue_service.run_async()
