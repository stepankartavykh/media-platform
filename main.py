from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
import os
from utils import start_processing


load_dotenv()


BOT_TOKEN = os.getenv('BOT_TOKEN')
START_URL = 'https://www.nytimes.com/'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    start_processing(START_URL)
    await update.message.reply_text('Start...')


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.run_polling()
