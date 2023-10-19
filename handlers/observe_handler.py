from telegram import Update
from telegram.ext import ContextTypes

from handlers.add_source_handler import current_sources


async def observe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sources = ''
    for index, source in enumerate(current_sources, start=1):
        sources += f'{index}. {source}\n'
    sources = ''.join(current_sources)
    await update.message.reply_text(
        f"""
        Observation just started...
        Your sources are:
        {sources}
        """
    )
