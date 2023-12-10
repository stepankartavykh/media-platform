from telegram import Update
from telegram.ext import ContextTypes


async def last_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Функционал разрабатывается...')
