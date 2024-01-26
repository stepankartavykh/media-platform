from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from database.queries import add_topic_query


mapper_button_callback_data_to_subjects = {
    'button_tech_news_new_topic': 'Tech news',
    'button_books_new_topic': 'Books',
    'button_movies_new_topic': 'Movies',
    'button_business_new_topic': 'Business',
    'button_research_physics_new_topic': 'Research (Physics)',
    'button_research_math_new_topic': 'Research (Math)',
    'button_research_health_new_topic': 'Research (Health)',
}

keyboard = [
    [InlineKeyboardButton(subject_name, callback_data=callback_data)]
    for callback_data, subject_name in mapper_button_callback_data_to_subjects.items()
]


topic_options = InlineKeyboardMarkup(keyboard)


async def add_topics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Введите интересную для вас тему.', reply_markup=topic_options)


async def action_on_click_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    topic = mapper_button_callback_data_to_subjects[query.data]
    add_topic_query(query.from_user.id, topic)
    await query.edit_message_text(text='Тема добавлена!')
    markup = query.message.reply_markup
    markup.inline_keyboard = None
    await query.edit_message_reply_markup(reply_markup=markup)
    # await query.edit_message_reply_markup(reply_markup=None)


async def add_topic_to_config(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    topic = update.message.text
    add_topic_query(update.message.from_user.id, topic)
    await update.message.reply_text('Тема добавлена!')
    return ConversationHandler.END
