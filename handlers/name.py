from aiohttp import Router, types
from aiogram.filters import Command

name_router = Router()


@name_router.message(Command('my_info'))
async def name(message: types.Message):
    await message.answer(f'ur first_name: {message.from_user.first_name}\
     nur id: {message.from_user.id}\nur username:@{message.from_user.username}')