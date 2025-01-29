from aiogram import Router, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import Database
from bot_config import database
from aiogram.filters import Command

catalog_router = Router()


@catalog_router.message(Command("catalog"))
async def show_catalog(message: types.Message, page: int = 1):
    limit = 5
    offset = (page - 1) * limit
    dishes = database.get_dishes(limit=limit, offset=offset)
    total_dishes = database.get_total_dishes()
    total_pages = (total_dishes + limit - 1) // limit

    if not dishes:
        await message.answer("Каталог пуст.")
        return

    text = "📌 Список блюд:\n\n"
    for dish in dishes:
        name, year, author, price, description, category, cover = dish
        text += (f"🍽 {name}\n📅 Год: {year}\n👨‍🍳 Шеф: {author}\n💰 Цена: {price} руб.\n"
                 f"📖 Описание: {description}\n🏷 Категория: {category}\n\n")
        if cover:
            await message.answer_photo(photo=cover, caption=text)
        else:
            await message.answer(text)

    keyboard = InlineKeyboardBuilder()
    if page > 1:
        keyboard.button(text="⬅️ Назад", callback_data=f"page_{page - 1}")
    if page < total_pages:
        keyboard.button(text="Вперед ➡️", callback_data=f"page_{page + 1}")

    if total_pages > 1:
        await message.answer("Страница {}/{}".format(page, total_pages), reply_markup=keyboard.as_markup())


@catalog_router.callback_query(lambda c: c.data.startswith("page_"))
async def pagination_handler(callback: types.CallbackQuery):
    page = int(callback.data.split("_")[1])
    await show_catalog(callback.message, page=page)
    await callback.answer()
