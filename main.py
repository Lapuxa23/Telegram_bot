
from asyncio import run
from bot_config import Bot,dp
from handlers.start import start_router
from handlers.random_name import random_router
from handlers.name import name_router
from handlers.capito import capito_router


async def main():
    dp.include_router(start_router)
    dp.include_router(random_router)
    dp.include_router(name_router)
    dp.include_router(capito_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
