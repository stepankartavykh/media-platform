import asyncio

import aiohttp
from telegram import Update
from telegram.ext import ContextTypes

from config import NEWS_API_KEY
from database.queries import get_topics


async def send_response_to_storage(response):
    return 1


def get_short_message(response, number_of_articles_to_consider=5):
    articles = response['articles']
    if len(articles):
        result_messages = []
        for article in articles[:number_of_articles_to_consider]:
            result_messages.append(article['title'] + '\n' + article['url'])
        return '\n'.join(result_messages)
    if len(response['articles']):
        return response['articles'][0]['title']
    else:
        return 'No articles found'


async def fetch_data(url, session):
    async with session.get(url) as response:
        return await response.json()


async def send_requests(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch_data(url, session))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses


async def observe_topics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    topics = get_topics(update.message.from_user.id)
    if not topics:
        await update.message.reply_text('There are no topics to monitor.')
    else:
        for topic in topics:
            await update.message.reply_text(topic)
        urls = ['https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'.format(query=topic,
                                                                                      api_key=NEWS_API_KEY)
                for topic in topics]
        responses = await send_requests(urls)
        for response in responses:
            await update.message.reply_text(get_short_message(response))


async def create_news_feed_from_topics(update: Update):
    pass
