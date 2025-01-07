import os
import random
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from aiogram.utils.exceptions import BotBlocked


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set in .env file.")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

names = ("Alice", "Bob", "Charlie", "Dave", "Eve", "Jona", "Mallory", "Trent")


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply(f"Привет, {message.from_user.first_name}!")


@dp.message_handler(commands=["myinfo"])
async def myinfo(message: types.Message):
    user = message.from_user
    await message.reply(
        f"Ваш ID: `{user.id}`\n"
        f"Ваше имя: `{user.first_name}`\n"
        f"Ваш username: `@{user.username}`",
        parse_mode=ParseMode.MARKDOWN_V2,
    )


@dp.message_handler(commands=["random"])
async def random_name(message: types.Message):
    name = random.choice(names)
    await message.reply(f"Случайное имя: {name}")


@dp.errors_handler()
async def error_handler(update: types.Update, exception: Exception):

    from aiogram.utils.exceptions import (
        MessageNotModified,
        MessageToDeleteNotFound,
        MessageTextIsEmpty,
        RetryAfter,
        TelegramAPIError,
    )
    if isinstance(exception, (BotBlocked, MessageNotModified, MessageToDeleteNotFound,
                              MessageTextIsEmpty, RetryAfter, TelegramAPIError)):
        return True
    print(f"Exception in {__file__}: {exception}")
    return True


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
