import asyncio

from loguru import logger

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
os.chdir(PROJECT_ROOT)
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.config import settings
from src.processing_worker.queue import run_in_process_pool


async def main() -> None:
    tasks = [run_in_process_pool(index) for index in range(1, settings.number_of_processes + 1)]
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError as e:
        logger.error(
            f"Cancelled error occured. Gracefully shutdown broker.\nTraceback:\n{e}"
        )
    except Exception as e:
        logger.error(f"Outer exception occured. Trying to restart...\nTraceback:\n{e}")
        # await main()


if __name__ == "__main__":
    asyncio.run(main())
