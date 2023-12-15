from telegram import Update
from telegram.ext import ContextTypes

from api.test_getiing_info import ApiEndpoint
from config import NEWS_API_KEY
from database.queries import get_topics


async def send_response_to_storage(response):
    return 1


def get_short_message(response):
    return 'default message'


async def observe_topics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    topics = get_topics(update.message.from_user.id)
    if not topics:
        await update.message.reply_text('There are no topics to monitor.')
    else:
        endpoints = [ApiEndpoint(url='https://newsapi.org/v2/everything',
                                 payload={
                                     'q': topic,
                                     'apiKey': NEWS_API_KEY,
                                 },
                                 api_type='everything')
                     for topic in topics]
        for endpoint in endpoints:
            response = await endpoint.get_api_async_response()
            short_message = get_short_message(response)
            await send_response_to_storage(response)
            await update.message.reply_text(short_message)
