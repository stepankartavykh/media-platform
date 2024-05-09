import asyncio

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from database import DBSession
from database.models import Topic
from database.services.topic.service import TopicService

mapper_button_callback_data_to_subjects = {
    'button_tech_news_new_topic': 'Tech news',
    'button_books_new_topic': 'Books',
    'button_movies_new_topic': 'Movies',
    'button_business_new_topic': 'Business',
    'button_research_physics_new_topic': 'Research (Physics)',
    'button_research_math_new_topic': 'Research (Math)',
    'button_research_health_new_topic': 'Research (Health)',
}


async def get_top_topics() -> list[Topic]:
    await asyncio.sleep(0.1)
    all_topics = DBSession.query(Topic).all()
    return all_topics


async def get_buttons_reply_markup() -> InlineKeyboardMarkup:
    topics: list[Topic] = await get_top_topics()
    keyboard = [[InlineKeyboardButton('checkbox', callback_data='qwer'),
                 InlineKeyboardButton(topic.name, callback_data=f"{topic.id}_topic_callback_data")]
                for topic in topics]
    keyboard.append([InlineKeyboardButton('Добавить выбранные темы.', callback_data='test_button')])
    return InlineKeyboardMarkup(keyboard)


async def add_topics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    topics_buttons = await get_buttons_reply_markup()
    await update.message.reply_text('Введите интересную для вас тему.', reply_markup=topics_buttons)
    return 'NEW_TOPIC'


async def button_coroutine(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    t = query.message.message_id
    print(t)
    print(query)
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    await add_topic_to_config(query.from_user.id, query.data)
    new_text = f'Тема {query.data} добавлена.'
    await context.bot.edit_message_text(chat_id=query.message.chat.id, message_id=t, text=new_text)


async def add_topic_to_config(user_id: int, chosen_topic: str) -> int:
    chosen_topic_id = chosen_topic.find('_')
    if chosen_topic_id in (0, -1):
        raise Exception(f'Wrong callback data <{chosen_topic}> for topic!')
    chosen_topic_id = int(chosen_topic[:chosen_topic_id])
    TopicService().add_topic_for_user_preference(user_id, chosen_topic_id)
    return ConversationHandler.END
