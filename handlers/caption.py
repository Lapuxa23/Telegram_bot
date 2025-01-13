import random
from bot_config import dp
from aiohttp import Router, types
from aiogram.filters import Command
capito_router = Router()
recipes = {
    "Салат": "images/salad.jpg",
    "Борщ": "images/borscht.jpg",
    "Пицца": "images/pizza.jpg"
}

@capito_router.message(Command("random_recipe"))
async def cmd_random_recipe(message: types.Message):
    dish = random.choice(list(recipes.keys()))
    photo_path = recipes[dish]
    with open(photo_path, 'rb') as photo:
        await message.answer_photo(photo, caption=f"Рецепт для: {dish}")
