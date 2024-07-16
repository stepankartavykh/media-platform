import asyncio
import json
import random
from enum import Enum
import aiohttp

from DataApp import DatabaseConfig
from DataApp.dataflow.send import MessageBrokerService
from api.get_news_dump import get_news_feed_everything
from api.interfaces.news_sources import EverythingResponseInterface, ArticleInterface
import asyncpg


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
    # print(f'article from {article.source} send to processing queue...')
    return MessageBrokerNotification.success


async def database_configure(article: ArticleInterface) -> int:
    await asyncio.sleep(1)
    print(f'article {article.url} configured with database...')
    return 1


class GroupClassification:
    pass


class MetricsObject:
    pass


MetricsType = tuple[GroupClassification, MetricsObject]


class ArticleMetricsInterface:
    # TODO definition of metrics in progress. For that we need to understand models that will be available in
    #  AnalysisApp.

    @classmethod
    def return_group_classification_and_metrics(cls, article: ArticleInterface) -> MetricsType:
        return GroupClassification(), MetricsObject()


async def extract_metrics_from_article(article: ArticleInterface) -> tuple[GroupClassification, MetricsObject]:
    # TODO Request to AnalysisApp service.
    return ArticleMetricsInterface.return_group_classification_and_metrics(article)


async def parse_article(session: aiohttp.client.ClientSession, article: ArticleInterface):
    params = {"url_list": [article.url],
              "headless": False,
              "readability": False}
    headers = {"Content-Type": "application/json"}
    async with session.post('http://127.0.0.1:4090/v1/scrape', data=json.dumps(params), headers=headers) as response:
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])
        json_response = await response.json()
        print("Body:", json_response['data'][0], "...")
    return json_response if json_response['msg'] == 'ok' else {}


insert_parsed_query = "insert into parsed.packets (packet) VALUES ({data_packet})"


async def process_article_in_pipeline(session: aiohttp.client.ClientSession, pool: asyncpg.pool.Pool,
                                      article: ArticleInterface) -> None:
    print("Processing " + article.url + "...")
    parsed_data = await parse_article(session, article)
    print(parsed_data)
    async with pool.acquire() as connection:
        connection.execute(insert_parsed_query.format(data_packet=json.dumps(parsed_data)))
    metrics_from_article = await extract_metrics_from_article(article)
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
        async with aiohttp.ClientSession() as session, asyncpg.create_pool(host=DatabaseConfig.host.value,
                                                                           port=DatabaseConfig.port.value,
                                                                           user=DatabaseConfig.user.value,
                                                                           password=DatabaseConfig.password.value,
                                                                           database=DatabaseConfig.database_name.value,
                                                                           min_size=1,
                                                                           max_size=6) as pool:
            for article in everything_on_topic.articles:
                articles_tasks.append(asyncio.create_task(process_article_in_pipeline(session, pool, article)))
            await asyncio.gather(*articles_tasks)
        await asyncio.sleep(interval)


def main():
    asyncio.run(data_pipeline_simulation(1))


if __name__ == '__main__':
    main()
