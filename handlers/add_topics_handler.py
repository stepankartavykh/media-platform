from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from database.queries import add_topic_query


async def add_topics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text('Введите интересную для вас тему.')
    return 'NEW_TOPIC'


async def add_topic_to_config(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    topic = update.message.text
    add_topic_query(update.message.from_user.id, topic)
    await update.message.reply_text('Тема добавлена!')
    return ConversationHandler.END
