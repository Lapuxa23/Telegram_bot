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


class Book(StatesGroup):
    name = State()
    year = State()
    author = State()
    price = State()
    cover = State()

@admin_menu_router.message(Command("add_dish"), default_state)
async def new_book(message: types.Message, state: FSMContext):
    await message.answer("Введите название блюда")
    message.from_user.id
    await state.set_state(Book.name)

@admin_menu_router.message(Book.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите год создания рецепта")
    await state.set_state(Book.year)

@admin_menu_router.message(Book.year)
async def process_year(message: types.Message, state: FSMContext):
    year = message.text
    if not year.isdigit():
        await message.answer("Вводите только цифры")
        return
    year = int(year)
    if year < 0 or year > 2025:
        await message.answer("Вводите только действительный год создания")
        return
    await state.update_data(year=message.text)
    await message.answer("Введите имя шеф-повара")
    await state.set_state(Book.author)

@admin_menu_router.message(Book.author)
async def process_author(message: types.Message, state: FSMContext):
    await state.update_data(author=message.text)
    await message.answer("Введите цену блюда")
    await state.set_state(Book.price)

@admin_menu_router.message(Book.price)
async def process_price(message: types.Message, state: FSMContext):
    price = message.text
    if not price.isdigit():
        await message.answer("Вводите только цифры")
        return
    price = int(price)
    if price <= 0:
        await message.answer("Вводите только положительную цену")
        return
    await state.update_data(price=price)
    await message.answer("Загрузите фото блюда")
    await state.set_state(Book.cover)

@admin_menu_router.message(Book.cover, F.photo)
async def process_cover(message: types.Message, state: FSMContext):
    covers = message.photo
    pprint(covers)
    biggest_image = covers[-1]
    await state.update_data(cover = biggest_image.file_id)
    await message.answer("Спасибо, блюдо было сохранено")
    data = await state.get_data()
    print(data)
    database.save_book(data)
    await state.clear()
