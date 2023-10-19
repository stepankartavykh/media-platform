from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


current_sources = []


async def add_source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text('Введите название ресурса, который вы хотите дополнительно отслеживать (URL):')
    return 'NEW_SOURCE'


def check_url_is_valid(url: str) -> bool:
    return True


async def get_source(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    source_url = update.message.text
    if check_url_is_valid(source_url):
        current_sources.append(source_url)
    else:
        await update.message.reply_text('Некорректный URL.')
    await update.message.reply_text('Источник добавлен!')

    return ConversationHandler.END
