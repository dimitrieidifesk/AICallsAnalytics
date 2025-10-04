from loguru import logger
from faststream.rabbit.broker import RabbitBroker
import aiormq.exceptions

from src.core.config import settings
from src.core.constants import QUEUE_PATH
from src.integrations.broker.schemas import CallSessionProcessingSchema


class RabbitBrokerManager:
    _broker: RabbitBroker

    def __init__(self, url: str):
        self._broker = RabbitBroker(url)

    async def publish(self, data: CallSessionProcessingSchema):
        try:
            async with self._broker as br:
                await br.publish(message=data, queue=QUEUE_PATH)
        except aiormq.exceptions.ChannelClosed as e:
            logger.error(f"Channel closed: {e}")
            raise
        except Exception as e:
            logger.error(f"Error publishing message: {e}")


broker = RabbitBrokerManager(settings.rabbit.url)
