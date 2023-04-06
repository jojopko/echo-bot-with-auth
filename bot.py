import logging
import os
import requests

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = os.getenv("BOT_TOKEN")
SERVER_HOST = os.getenv("SERVER_HOST")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"http://{SERVER_HOST}/check-user"
    response = requests.get(url,
                            params={"user_id": update.effective_user.id})
    if "Authorized" in response.text:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Hi, you are Authorized user!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Oh... You are no authorized user. Use `/login` if you want use this bot.")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"http://{SERVER_HOST}/check-user"
    response = requests.get(url,
                            params={"user_id": update.effective_user.id})
    if "Authorized" in response.text:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=update.message.text)

async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = f"http://{SERVER_HOST}/sign-up"
    response = requests.get(url,
                            params={"user_id": update.effective_user.id,
                                    "user_name": update.effective_user.first_name,
                                    "password": update.message.text.split(" ", 1)[1].strip()})
    print(response)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    login_handler = CommandHandler('login', login)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(login_handler)

    application.run_polling()

