import asyncio
import json
import random
import time
from enum import Enum

import aiohttp
from fastapi.encoders import jsonable_encoder

from sqlalchemy.engine import Row

from cache_plugin import AsyncCacheSystemPlugin
from database_storage_plugin import AsyncDatabaseStoragePlugin
from interface_data import DataPacketInterface, AddArticleInterface, UpdateArticleInterface, \
    AllDataStartState
from api.get_news_dump import get_news_feed_everything
from DataApp.storage_schemas.storage import Article, engine
from sqlalchemy.orm import Session
from aiohttp import ClientSession


CacheSystemResponse: type = tuple[int, str]
OperationType: type = str


class OperationChangeFrontendState(Enum):
    """Enumeration for types of operations."""

    start = 'start'
    update = 'update'


class ActualContent:
    def __init__(self, operation_type: OperationType, data: DataPacketInterface | AllDataStartState):
        self.operation = operation_type
        self.data = data

    def convert_data(self) -> str:
        return str(type(self.data).model_dump(self.data))


cache_system_plugin = AsyncCacheSystemPlugin()
database_plugin = AsyncDatabaseStoragePlugin()


def serialize_item(item: Row) -> dict:
    return {
        "id": item.id,
        "priority": item.priority,
        "shortTitle": item.short_title,
        "shortDescription": item.short_description,
        "blockContent": []
    }


async def get_current_content(start_load: bool = False, get_from_cache_directly: bool = False) -> ActualContent:
    if get_from_cache_directly:
        content = await cache_system_plugin.get_actual_content()
        arts = []
        for obj in content:
            arts.append(AddArticleInterface.model_validate_json(str(obj).replace("'", '"')))
        content = DataPacketInterface(articlesAdd=arts,
                                      articlesUpdate=[])
        return ActualContent(operation_type='update', data=content)
    content = await database_plugin.get_actual_content()
    content_start_state = AllDataStartState(blocks=[serialize_item(item) for item in content])
    actual_content = ActualContent(operation_type='start', data=content_start_state)
    return actual_content


async def send_articles_to_cache_system(articles: list[AddArticleInterface]) -> CacheSystemResponse:
    await cache_system_plugin.send_data([art.model_dump() for art in articles])
    return 200, 'success'


async def fetch_status(session: ClientSession, url: str) -> (int, str):
    try:
        async with session.get(url) as result:
            return result.status, url
    except aiohttp.client_exceptions.ClientConnectorError:
        return 400, 'ClientConnectorError'
    except aiohttp.client_exceptions.ServerDisconnectedError:
        return 400, 'ServerDisconnectedError'
    except aiohttp.client_exceptions.TooManyRedirects:
        return 300, 'TooManyRedirects'


def define_topic_for_api_call() -> str:
    possible_topics = ["economics", "microelectronics", "quantum computing", "investing", "research technologies",
                       "medicine", "water desalination", "physics", "economics reports", "microchips new research",
                       "power", "new sources energy", "energy sources", "energy storage devices", "clean energy",
                       "energy power investments", "investing strategies"]
    if not possible_topics:
        possible_topics.append("news")
    return random.choice(possible_topics)


def generate_article_to_add(data_article) -> AddArticleInterface:
    return AddArticleInterface(source=data_article.get('source', {'name': "Unknown"}).get('name'),
                               priority=random.randint(1, 10),
                               author=data_article.get('author', 'Unknown'),
                               title=data_article.get('title', 'Unknown'),
                               description=data_article.get('description', 'None'),
                               url=data_article.get('url'),
                               publishedAt=data_article.get('publishedAt'),
                               content=data_article.get('content'))


def generate_article_to_database_storage(data_article) -> Article:
    return Article(author=data_article.get('author', 'Unknown'),
                   title=data_article.get('title', 'Unknown'),
                   description=data_article.get('description', 'None'),
                   content=data_article.get('content'),
                   published_at=data_article.get('publishedAt'),
                   url=data_article.get('url'))


def generate_article_to_update(data_article):
    return UpdateArticleInterface(update_type=random.choice(('update', 'add_content', 'replace')),
                                  priority=random.randint(1, 10),
                                  source=data_article.get('source', {'name': "Unknown"}).get('name'),
                                  author=data_article.get('author', 'Unknown'),
                                  title=data_article.get('title', 'Unknown'),
                                  description=data_article.get('description', 'None'),
                                  url=data_article.get('url'),
                                  urlToImage=data_article.get('urlToImage'),
                                  publishedAt=data_article.get('publishedAt'),
                                  content=data_article.get('content'))


async def generate_article_content(from_api: bool = True, consider_amount: int | None = None) -> DataPacketInterface:
    if not from_api:
        raise NotImplementedError('Implementation of dump load is required!')
    extracted_data_path = get_news_feed_everything(topic=define_topic_for_api_call())
    with open(extracted_data_path, 'r') as f:
        data = json.load(f)
    print('data dump is loaded from external API')
    articles_to_add = []
    articles_to_update = []
    articles_to_database = []
    if not consider_amount:
        consider_amount = len(data['articles'])
    with Session(engine) as session:
        all_articles_urls = [art[0] for art in session.query(Article.url).all()]
    all_articles_urls = set(all_articles_urls)
    print(all_articles_urls)
    all_urls = [art.get('url') for art in data['articles'][:consider_amount]]
    filtered_urls = set()
    async with ClientSession() as session:
        tasks = []
        for url in all_urls:
            tasks.append(asyncio.create_task(fetch_status(session, url)))
        while tasks:
            done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for done_task in done:
                res = await done_task
                if done_task.exception() is None:
                    status, url = res
                    if status == 200:
                        filtered_urls.add(url)
            # TODO Figure out what to do with "bad" urls.
    for data_article in data['articles'][:consider_amount]:
        if data_article.get('url') in all_articles_urls:
            print('Same article!')
            continue
        if data_article.get('url') not in filtered_urls:
            continue
        if random.randint(1, 10) < 6:
            add_article = generate_article_to_add(data_article)
            articles_to_database.append(generate_article_to_database_storage(data_article))
            articles_to_add.append(add_article)
        else:
            update_article = generate_article_to_update(data_article)
            articles_to_update.append(update_article)
    # await send_articles_to_cache_system(articles_to_add)
    content_packet = DataPacketInterface(articlesAdd=articles_to_add,
                                         articlesUpdate=articles_to_update)
    with open(f'/home/skartavykh/MyProjects/media-bot/storage/data_packets/{time.time_ns()}.json', 'w') as f:
        json.dump(jsonable_encoder(content_packet), f)
    with Session(engine) as session:
        session.add_all(articles_to_database)
        session.commit()
    return content_packet


if __name__ == '__main__':
    actual_content: ActualContent = asyncio.run(get_current_content())
    print(actual_content.convert_data())
