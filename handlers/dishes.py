from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot_config import Database


class AddDish(StatesGroup):
    name = State()
    price = State()
    description = State()
    category = State()
    portion_options = State()


admin_menu_router = Router()


@admin_menu_router.message(Command("add_dish"))
async def add_dish_start(message: types.Message, state: FSMContext):
    if message.from_user.id == 1103706734:
        await message.answer("Введите название блюда:")
        await state.set_state(AddDish.name)
    else:
        await message.answer("У вас нет прав для этой команды.")


@admin_menu_router.message(AddDish.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите цену:")
    await state.set_state(AddDish.price)


@admin_menu_router.message(AddDish.price)
async def process_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
        await state.update_data(price=price)
        await message.answer("Введите описание:")
        await state.set_state(AddDish.description)
    except ValueError:
        await message.reply("Цена должна быть числом.")


@admin_menu_router.message(AddDish.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    categories = [
        "первое", "второе", "пицца", "горячие напитки", "холодные напитки", "салаты", "горячительные напитки"
    ]
    kb = types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text=c)] for c in categories], resize_keyboard=True,
                                   one_time_keyboard=True)
    await message.answer("Выберите категорию:", reply_markup=kb)

    await state.set_state(AddDish.category)


@admin_menu_router.message(AddDish.category)
async def process_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Введите варианты порций (через запятую, например: 'маленькая, средняя, большая'):",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddDish.portion_options)


@admin_menu_router.message(AddDish.portion_options)
async def process_portion_options(message: types.Message, state: FSMContext):
    await state.update_data(portion_options=message.text)
    data = await state.get_data()
    await message.answer(
        f"<b>Проверяем данные перед сохранением:</b>\n"
        f"Название: {data['name']}\n"
        f"Цена: {data['price']}\n"
        f"Описание: {data['description']}\n"
        f"Категория: {data['category']}\n"
        f"Порции: {data['portion_options']}" , parse_mode="HTML"
    )

    db = Database("restaurant.db")
    try:
        if db.dishes_review(data):
            await message.answer("<b>Блюдо успешно добавлено!</b>", parse_mode="HTML")
        else:
            await message.answer("<b>Не удалось добавить блюдо. Произошла ошибка при записи в базу данных.</b>", parse_mode="HTML")
    except Exception as e:
        await message.answer(f"<b>Произошла ошибка:</b> <code>{e}</code>", parse_mode="HTML")
    finally:
        db.close()
        await state.clear()
