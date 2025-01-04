import os
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable not set in .env file.")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Привет, {update.effective_user.first_name}!")


async def myinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Ваш id: {user.id}\nВаше имя: {user.first_name}\n"
                                        f"Ваш username: @{user.username}")


names = ("Alice", "Bob", "Charlie", "Dave", "Eve")


async def random_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = random.choice(names)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Случайное имя: {name}")


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    myinfo_handler = CommandHandler('myinfo', myinfo)
    random_handler = CommandHandler('random', random_name)

    application.add_handler(start_handler)
    application.add_handler(myinfo_handler)
    application.add_handler(random_handler)

    application.run_polling()

