from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import datetime

from bot_config import database


class RestaurantReview(StatesGroup):
    name = State()
    contact = State()
    visit_date = State()
    rating = State()
    extra_comments = State()


review_router = Router()


@review_router.callback_query(F.data== "review")
async def review_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Как вас зовут?")
    await state.set_state(RestaurantReview.name)


@review_router.message(RestaurantReview.name)
async def process_name(m:types.Message,state:FSMContext):
    await m.answer("ваш контакт")
    await state.set_state(RestaurantReview.contact)


@review_router.message(RestaurantReview.contact)
async def process_name(m:types.Message,state:FSMContext):
    await m.answer("ваша дата визита")
    await state.set_state(RestaurantReview.visit_date)


@review_router.message(RestaurantReview.visit_date)
async def process_visit_date(message: types.Message, state: FSMContext):
    if message.text.lower() != "пропустить":
        try:
            visit_date = datetime.datetime.strptime(message.text, "%Y-%m-%d").date()
            await state.update_data(visit_date=str(visit_date))
        except ValueError:
            await message.reply(
                "Неверный формат даты. Пожалуйста, используйте формат ГГГГ-ММ-ДД или напишите 'пропустить'.")
            return

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=str(i), callback_data=f"rating:{i}") for i in range(1, 6)]
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

    try:

        database.save_review(data)
        await message.answer(f"Спасибо за ваш отзыв, {data['name']}!")
        await state.clear()

    except Exception as e:
        await message.answer("Произошла ошибка при сохранении отзыва. Пожалуйста, попробуйте позже.")
        print(f"Error saving review: {e}")
        await state.clear()
