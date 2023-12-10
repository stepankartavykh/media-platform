from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from database.queries import add_source_query
from utils.request_handler import get_status_code


async def add_source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text('Введите название ресурса, который вы хотите дополнительно отслеживать (URL):')
    return 'NEW_SOURCE'


def check_url_is_valid(url: str) -> bool:
    if get_status_code(url) == 200:
        return True
    return False


async def get_source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    source_url = update.message.text
    if check_url_is_valid(source_url):
        add_source_query(update.message.from_user.id, source_url)
        await update.message.reply_text('Источник добавлен!')
    else:
        await update.message.reply_text('Некорректный URL.')
    return ConversationHandler.END
