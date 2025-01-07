from dotenv import dotenv_values
from aiogram import Bot, Dispatcher,types
from asyncio import run
from aiogram.filters import Command
import random

token = dotenv_values('.env')['TOKEN']
bot = Bot(token=token)
dp = Dispatcher()

names = ('name', 'Azamat', 'Timur')


@dp.message(Command('start'))
async def start(message:types.Message):
    await message.answer(f'hello {message.from_user.first_name}')


@dp.message(Command('my_info'))
async def name(message:types.Message):
    await message.answer(f'ur first_name: {message.from_user.first_name}\
    nur id: {message.from_user.id}\nur username:@{message.from_user.username}')


@dp.message(Command('random'))
async def random_name(message:types.Message):
    random_name = random.choice(names)
    await message.answer(random_name)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    run(main())
