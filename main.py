import asyncio
import logging
from aiogram import Bot

from bot_config import bot, dp, database
from handlers.start import start_router
from handlers.dishes import admin_menu_router
from handlers.catalog import catalog_router
from handlers.caption import picture_router
from handlers.review_dialog import review_router
from handlers.admin import admin_router
from handlers.other_messages import other_router




async def on_startup(bot: Bot):
    database.create_tables()


async def main():
    dp.include_router(start_router)
    dp.include_router(picture_router)
    dp.include_router(admin_router)
    dp.include_router(review_router)
    dp.include_router(admin_menu_router)
    dp.include_router(catalog_router)

    dp.startup.register(on_startup)
    dp.include_router(other_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
