from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


class UserFeedback(StatesGroup):
    name = State()
    age = State()
    feedback = State()


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
                types.InlineKeyboardButton(text="Обратная связь", callback_data="feedback"),
                types.InlineKeyboardButton(text="Оставить отзыв", callback_data="review"), # Callback for review
            ],
            [
                types.InlineKeyboardButton(text="Корзина", callback_data="cart"),
                types.InlineKeyboardButton(text="Реклама", callback_data="ads"),
            ],

        ]
    )
    await message.answer(f"Привет, {name}! Добро пожаловать в наш ресторан!", reply_markup=kb)







@start_router.callback_query(F.data == "review")
async def review_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Как вас зовут?", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(UserFeedback.name)


@start_router.message(UserFeedback.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько вам лет?")
    await state.set_state(UserFeedback.age)


@start_router.message(UserFeedback.age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age > 0 :
            await state.update_data(age=age)
            await message.answer("Оставьте свой отзыв:")
            await state.set_state(UserFeedback.feedback)
        else:
            await message.answer("Пожалуйста, введите корректный возраст.")


    except ValueError:
         await message.answer("Пожалуйста, введите число.")




@start_router.message(UserFeedback.feedback)
async def process_feedback(message: types.Message, state: FSMContext):
    await state.update_data(feedback=message.text)
    data = await state.get_data()
    await message.answer(f"Спасибо за ваш отзыв, {data['name']}!\n"
                           f"Ваш возраст: {data['age']}\n"
                           f"Ваш отзыв: {data['feedback']}")
    await state.clear()


