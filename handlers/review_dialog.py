from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot_config import database
from handlers.start import start_router


class RestaurantReview(StatesGroup):
    name = State()
    contact = State()
    rating = State()
    extra_comments = State()
    visit_date = State()
review_router = Router()

@review_router.callback_query(Command("review"))
async def review_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Как вас зовут?")
    await state.set_state(RestaurantReview.name)


@review_router.message(RestaurantReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Ваш номер телефона или имя пользователя Instagram?")
    await state.set_state(RestaurantReview.contact)


@review_router.message(RestaurantReview.contact)
async def process_contact(message: types.Message, state: FSMContext):
    await state.update_data(contact=message.text)
    await message.answer("Когда вы посетили наш ресторан? (Необязательно, формат: ГГГГ-ММ-ДД)")
    await state.set_state(RestaurantReview.visit_date)


@review_router.message(RestaurantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    if message.text.lower() != "пропустить":
        try:
            await state.update_data(visit_date=str(visit_date))
        except ValueError:
            await message.reply(
                "Неверный формат даты. Пожалуйста, используйте формат ГГГГ-ММ-ДД или напишите 'пропустить'.")
            return

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text='1', callback_data='rating:1'),
                types.InlineKeyboardButton(text='2', callback_data='rating:2'),
                types.InlineKeyboardButton(text='3', callback_data='rating:3'),
                types.InlineKeyboardButton(text='4', callback_data='rating:4'),
                types.InlineKeyboardButton(text='5', callback_data='rating:5'),
            ]
        ]
    )
    await message.answer("Поставьте нам оценку:", reply_markup=kb)
    await state.set_state(RestaurantReview.rating)


@review_router.callback_query(RestaurantReview.rating)
async def process_rating(callback: types.CallbackQuery, state: FSMContext):
    rating = int(callback.data.split(":")[1])
    await state.update_data(rating=rating)
    await callback.answer()
    await callback.message.answer("Дополнительные комментарии/жалобы? (Необязательно)")
    await state.set_state(RestaurantReview.extra_comments)


@review_router.message(RestaurantReview.extra_comments)
async def process_extra_comments(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    data = await state.get_data()

    await message.answer(f"Спасибо за ваш отзыв, {data['name']}!")
    data = await state.get_data()
    print(data)
    database.save_complaint(data)
    await state.clear()