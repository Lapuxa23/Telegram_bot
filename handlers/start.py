from aiogram import Router, types
from aiogram.filters import Command

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Наш сайт", url="https://geeks.kg"),
                types.InlineKeyboardButton(text="Наш инстаграм", url="https://instagram.com"),
            ],
            [
                types.InlineKeyboardButton(text="О нас", callback_data="about_us"),
                types.InlineKeyboardButton(text="Меню", callback_data="menu"),
            ],
            [
                types.InlineKeyboardButton(text="Обратная связь", callback_data="review_dialog"
                                           ),

            ],
            [
                types.InlineKeyboardButton(text="Корзина", callback_data="cart"),
                types.InlineKeyboardButton(text="Реклама", callback_data="ads"),
            ],

        ]
    )
    await message.answer(f"Привет, {name}! Добро пожаловать в наш ресторан!", reply_markup=kb)
