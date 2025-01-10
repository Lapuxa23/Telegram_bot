from dotenv import dotenv_values
from aiogram import Bot, Dispatcher, types
from asyncio import run
from aiogram.filters import Command
import random

from hendlers.start import start_router
from hendlers.start import random_router
from hendlers.start import name_router
from hendlers.start import capito_router
token = dotenv_values('.env')['TOKEN']
bot = Bot(token=token)
dp = Dispatcher()

names = ('name', 'Azamat', 'Timur')


async def main():
    dp.include_router(start_router)
    dp.include_router(random_router)
    dp.include_router(name_router)
    dp.include_router(capito_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
