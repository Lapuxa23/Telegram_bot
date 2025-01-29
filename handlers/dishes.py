from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from pprint import pprint

from database import Database
from bot_config import database

admin_menu_router = Router()
admin_menu_router.message.filter(
    F.from_user.id == 1103706734
)

class Dish(StatesGroup):
    name = State()
    year = State()
    author = State()
    price = State()
    description = State()
    category = State()
    cover = State()

@admin_menu_router.message(Command("add_dish"), default_state)
async def new_dish(message: types.Message, state: FSMContext):
    await message.answer("Введите название блюда")
    await state.set_state(Dish.name)

@admin_menu_router.message(Dish.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите год создания рецепта")
    await state.set_state(Dish.year)

@admin_menu_router.message(Dish.year)
async def process_year(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Вводите только цифры")
        return
    year = int(message.text)
    if year < 0 or year > 2025:
        await message.answer("Введите корректный год")
        return
    await state.update_data(year=year)
    await message.answer("Введите имя шеф-повара")
    await state.set_state(Dish.author)

@admin_menu_router.message(Dish.author)
async def process_author(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await message.answer("Введите цену блюда")
    await state.set_state(Dish.price)

@admin_menu_router.message(Dish.price)
async def process_price(message: types.Message, state: FSMContext):
    if not message.text.replace('.', '', 1).isdigit():
        await message.answer("Введите корректную цену")
        return
    price = float(message.text)
    if price <= 0:
        await message.answer("Цена должна быть положительной")
        return
    await state.update_data(price=price)
    await message.answer("Введите описание блюда")
    await state.set_state(Dish.description)

@admin_menu_router.message(Dish.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите категорию блюда")
    await state.set_state(Dish.category)

@admin_menu_router.message(Dish.category)
async def process_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Загрузите фото блюда")
    await state.set_state(Dish.cover)

@admin_menu_router.message(Dish.cover, F.photo)
async def process_cover(message: types.Message, state: FSMContext):
    biggest_image = message.photo[-1]
    await state.update_data(cover=biggest_image.file_id)
    data = await state.get_data()
    database.save_dish(data)
    await message.answer("Спасибо, блюдо сохранено!")
    await state.clear()