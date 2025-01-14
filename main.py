import asyncio
import logging

from bot_config import Bot, dp
from handlers.start import start_router
from handlers.random import random_router
from handlers.name import name_router
#from handlers.caption import capito_router


async def main():
    dp.include_router(start_router)
    dp.include_router(random_router)
    dp.include_router(name_router)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
