from dotenv import dotenv_values
from aiogram import Bot, Dispatcher, types
from asyncio import run
from aiogram.filters import Command
import random
from bot_config import bot, dp
from hendlers.start import start_router
from hendlers.random_name  import random_router
from hendlers.name import name_router
from hendlers.capito import capito_router

names = ('name', 'Azamat', 'Timur')


async def main():
    dp.include_router(start_router)
    dp.include_router(random_router)
    dp.include_router(name_router)
    dp.include_router(capito_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
