from telegram import Update
from telegram.ext import ContextTypes
from telegram import User as TelegramUser

from database.services.user.service import UserService
from messages import START_GREETINGS_RUS


async def auth_user(user: TelegramUser) -> None:
    user_id, username = user.id, user.username
    UserService().add_user(user_id, username)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await auth_user(update.message.from_user)
    await update.message.reply_text(START_GREETINGS_RUS)
