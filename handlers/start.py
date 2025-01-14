from aiogram import Router, F, types
from aiogram.filters import Command

start_router = Router()



@start_router.message(Command("start"))
async def start_handler(message: types.Message):
    name = message.from_user.first_name
    kb = InlineKeyboardMarkup(
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
                types.InlineKeyboardButton(text="Обратная связь", callback_data="feedback"),
                types.InlineKeyboardButton(text="Оставить отзыв", callback_data="review"),
            ],
            [
                types.InlineKeyboardButton(text="Корзина", callback_data="cart"),
                types.InlineKeyboardButton(text="Реклама", callback_data="ads"),
            ],

        ]
    )
    await message.answer(f"Привет, {name}! Добро пожаловать в наш ресторан!", reply_markup=kb)



@start_router.callback_query(F.data == "about_us")
async def about_us_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Мы - ресторан с лучшими блюдами!")

@start_router.callback_query(F.data == "menu")
async def menu_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Вот наше меню:\n(Здесь будет меню)")

@start_router.callback_query(F.data == "feedback")
async def feedback_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Напишите нам свои вопросы или пожелания.")



@start_router.callback_query(F.data == "cart")
async def cart_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Ваша корзина пуста.")


@start_router.callback_query(F.data == "ads")
async def ads_handler(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("Здесь будет реклама.")


