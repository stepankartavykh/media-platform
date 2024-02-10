from telegram import Update
from telegram.ext import ContextTypes

from database.queries import get_sources
from utils import start_async_processing


async def observe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current_sources = get_sources(update.message.from_user.id)
    if not current_sources:
        await update.message.reply_text('There are no sources to monitor.')
    else:
        sources = ''
        for index, source in enumerate(current_sources, start=1):
            sources += f'{index}. {source}\n'
        sources = ''.join(current_sources)
        message = "Observation just started...Your sources:"
        await update.message.reply_text(message)
        await update.message.reply_text(sources)
        await start_async_processing(current_sources, update)
