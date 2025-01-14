from aiogram import Router, types
from aiogram.filters import Command

picture_router = Router()


@picture_router.message(Command("picture"))
async def send_picture_handler(message: types.Message):
    Pizza_images = types.FSInputFile("images/Pizza.jpg")
    await message.answer_photo(
        photo=Pizza_images,
        caption="Italia pizza"
    )