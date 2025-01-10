from aiogram import bot, Dispatcher
from dotenv import dotevn_values, dotenv_values

token = dotenv_values(".env") ["TOKEN"]
bot = BOT(token=token)
dp = Dispatcher