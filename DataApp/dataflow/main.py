import asyncio
import json
import random
from enum import Enum

from DataApp.dataflow.send import MessageBrokerService
from api.get_news_dump import get_news_feed_everything
from api.interfaces.news_sources import EverythingResponseInterface, ArticleInterface


class MessageBrokerNotification(Enum):
    success = 1
    error = 0


def define_topic_for_api_call() -> str:
    possible_topics = ["economics", "microelectronics", "quantum computing", "investing", "research technologies",
                       "medicine", "water desalination"]
    if not possible_topics:
        possible_topics.append("news")
    return random.choice(possible_topics)


async def send_to_message_broker(article: ArticleInterface) -> MessageBrokerNotification:
    await asyncio.sleep(0.1)
    MessageBrokerService.send_message(article.url)
    print(f'article from {article.source} send to processing queue...')
    return MessageBrokerNotification.success


async def database_configure(article: ArticleInterface) -> int:
    await asyncio.sleep(1)
    print(f'article {article.url} configured with database...')
    return 1


async def process_article_in_pipeline(article: ArticleInterface) -> None:
    print("Processing" + article.url + "...")
    send_to_message_broker_task = asyncio.create_task(send_to_message_broker(article))
    config_database_task = asyncio.create_task(database_configure(article))
    await asyncio.gather(send_to_message_broker_task,
                         config_database_task)


async def data_pipeline_simulation(count_times: int = 2, interval: int = 10) -> None:
    for i in range(count_times):
        topic = define_topic_for_api_call()
        dump_path = get_news_feed_everything(topic)
        with open(dump_path, 'r') as f:
            data = json.load(f)
        everything_on_topic = EverythingResponseInterface.model_validate(data)
        articles_tasks = []
        for article in everything_on_topic.articles:
            articles_tasks.append(asyncio.create_task(process_article_in_pipeline(article)))
        await asyncio.gather(*articles_tasks)
        await asyncio.sleep(interval)


def main():
    asyncio.run(data_pipeline_simulation(1))


if __name__ == '__main__':
    main()
