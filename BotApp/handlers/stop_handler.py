from telegram import Update
from telegram.ext import ContextTypes, ApplicationHandlerStop


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Выдача завершена.')
    print('message for debug')
    raise ApplicationHandlerStop()
