from aiogram import Router, types, F
from aiogram.types import ChatMemberUpdated, ChatPermissions
from aiogram.filters import Command
from datetime import datetime, timedelta
from aiogram.exceptions import TelegramBadRequest

admin_router = Router()


FORBIDDEN_WORDS = {"xd", "xd", "xd"}

def parse_time(time_str: str):
    units = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    try:
        unit = time_str[-1]
        value = int(time_str[:-1])
        return value * units.get(unit, 60)
    except ValueError:
        return 600

@admin_router.message(F.chat.type.in_({"group", "supergroup"}))
async def check_message(message: types.Message):

    if any(word in message.text.lower() for word in FORBIDDEN_WORDS):
        try:
            await message.chat.ban_member(user_id=message.from_user.id)
            await message.answer(f"{message.from_user.first_name} был забанен за использование запрещенных слов.")
        except TelegramBadRequest:
            await message.answer("Не удалось забанить пользователя.")

@admin_router.message(Command("ban"))
async def ban_user(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.answer("Использование: /ban @username [время]")
        return

    mention = args[1]
    duration = parse_time(args[2]) if len(args) > 2 else 600

    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif mention.startswith("@"):
        user_id = (await message.chat.get_member_by_username(mention[1:])).user.id
    else:
        await message.answer("Некорректное использование команды.")
        return

    try:
        until_date = datetime.now() + timedelta(seconds=duration)
        await message.chat.ban_member(user_id=user_id, until_date=until_date)
        await message.answer(f"Пользователь {mention} забанен на {duration // 60} минут.")
    except TelegramBadRequest:
        await message.answer("Не удалось забанить пользователя.")
