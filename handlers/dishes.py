from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot_config import Database
from typing import List, Dict, Tuple
import math


class AddDish(StatesGroup):


    admin_menu_router = Router()


async def show_dishes_page(message: types.Message, page: int, db: Database):
    dishes_per_page = 5
    offset = (page - 1) * dishes_per_page
    total_dishes = db.get_dishes_count()
    total_pages = math.ceil(total_dishes / dishes_per_page)

    if 1 <= page <= total_pages:
        dishes = db.get_dishes_paginated(offset, dishes_per_page)
        text = f"<b>Меню (страница {page}/{total_pages}):</b>\n\n"

        for dish in dishes:
            text += (f"<b>Название:</b> {dish['name']}\n"
                     f"<b>Цена:</b> {dish['price']}\n"
                     f"<b>Описание:</b> {dish['description']}\n"
                     f"<b>Категория:</b> {dish['category']}\n"
                     f"<b>Порции:</b> {dish['portion_options']}\n"
                     f"{'<b>Фото:</b> Есть' if dish.get('photo') else 'Фото: Нет'}\n\n")

        kb = types.InlineKeyboardMarkup(row_width=5)
        buttons = []

        for p in range(1, total_pages + 1):
            buttons.append(types.InlineKeyboardButton(text=str(p), callback_data=f"show_page:{p}"))
        kb.add(*buttons)

        await message.answer(text, parse_mode="HTML", reply_markup=kb)
    else:
        await message.answer("Такой страницы не существует.")


@admin_menu_router.message(Command("menu"))
async def show_menu(message: types.Message):
    db = Database("restaurant.db")
    await show_dishes_page(message, 1, db)
    db.close()


@admin_menu_router.callback_query(F.data.startswith("show_page:"))
async def handle_pagination(callback: types.CallbackQuery):
    page = int(callback.data.split(":")[1])
    db = Database("restaurant.db")
    await show_dishes_page(callback.message, page, dbe
    db.close()
    await callback.answer()


@admin_menu_router.message(AddDish.portion_options)
async def process_portion_options(message: types.Message, state: FSMContext):
