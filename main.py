import os
import random
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set in .env file.")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


names = ("Alice", "Bob", "Charlie", "Dave", "Eve", "Jona", "Mallory", "Trent")

@dp.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await message.reply(f"Привет, {message.from_user.first_name}!")


@dp.message(Command("myinfo"))
async def cmd_myinfo(message: types.Message, state: FSMContext):
    user = message.from_user
    await message.reply(
        f"Ваш ID: `{user.id}`\n"
        f"Ваше имя: `{user.first_name}`\n"
        f"Ваш username: `@{user.username}`",
        parse_mode=ParseMode.MARKDOWN_V2,
    )

@dp.message(Command("random"))
async def cmd_random(message: types.Message, state: FSMContext):
    name = random.choice(names)
    await message.reply(f"Случайное имя: {name}")

@dp.errors_handler()
async def error_handler(update: types.Update, exception: Exception):
    from aiogram.utils.exceptions import (
        BotBlocked,
        MessageNotModified,
        MessageToDeleteNotFound,
        MessageTextIsEmpty,
        RetryAfter,
        TelegramAPIError,
    )

    if isinstance(exception, (BotBlocked, MessageNotModified, MessageToDeleteNotFound,
                              MessageTextIsEmpty, RetryAfter, TelegramAPIError)):
        return True
    print(f"Error in {__file__}: {exception}")
    return True


if __name__ == "__main__":
    dp.run_polling()


