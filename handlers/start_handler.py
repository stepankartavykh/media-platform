import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from config import MAIN_DIR, DATABASE_PATH
from database.queries import add_user_query, get_user, create_database_with_tables
from messages import START_GREETINGS_RUS


async def auth_user(update: Update):
    user_id, username = update.message.from_user.id, update.message.from_user.username
    if not get_user(user_id):
        add_user_query(user_id, username)


def check_database():
    path_to_check = MAIN_DIR + DATABASE_PATH
    if not os.path.exists(path_to_check):
        create_database_with_tables()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    check_database()
    await auth_user(update)
    await update.message.reply_text(START_GREETINGS_RUS)


async def button_coroutine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")
