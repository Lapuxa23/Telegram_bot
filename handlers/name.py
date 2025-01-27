from aiogram import Router, types
from aiogram.filters import Command

name_router = Router()


@name_router.message(Command("name"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
