import random
from aiogram import Router, types
from aiogram.filters import Command

random_router = Router()


@random_router.message(Command('random'))
async def random_name(message: types.Message):
    random_name = random.choice(names)
    await message.answer(random_name)

names=['timur']
