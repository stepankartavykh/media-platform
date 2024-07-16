# TODO establish cache system functions. What are they?
"""
1. Insert data into cache. In what section you would insert entry? What the whole structure of Cache system?
2. Retrieve data from specific source.
3. Delete entry.
4. Update entry. Include functions to update by specific fields.
"""
import asyncio
import datetime
import json
import os.path
from enum import Enum
from typing import NewType

import redis
from redis import Redis
from redis.asyncio import Redis as AsyncioRedis
from api.get_news_dump import get_news_from_news_data_io, get_news_feed_everything
from DataApp.config import REDIS_PORT, REDIS_HOST, LOCAL_STORAGE_PATH


def get_filenames_with_dump() -> list[str]:
    return ['bloomberg_quint_news.json']


REDIS_SECTIONS_COUNT = 16
REDIS_SECTION_WITH_BLOCKS = 0
REDIS_SECTION_BLOCK_INFO = 1


class SectionsDistribution(Enum):
    economics = "economics"
    physics_research = "physics research"
    investing = "investing"


class AsyncCacheSystem:
    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT, db_section: int = 0):
        self._redis = AsyncioRedis(host=host,
                                   port=port,
                                   db=db_section,
                                   decode_responses=True)


class CacheSystem:
    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT, db_sections: int = REDIS_SECTIONS_COUNT):
        self._redis: dict[int, redis.client.Redis] = {section: Redis(host=host,
                                                                     port=port,
                                                                     db=section,
                                                                     decode_responses=True)
                                                      for section in range(db_sections)}
        self.default_section = 0
        self.available_sections = list(range(REDIS_SECTIONS_COUNT))

    def load_initial_data(self) -> None:
        redis_client = self._redis[0]
        initial_dump_path = '/home/skartavykh/MyProjects/media-bot/storage/initial_articles/initial.json'
        if os.path.exists(initial_dump_path) and initial_dump_path.endswith('.json'):
            with open(initial_dump_path) as f:
                data = json.load(f)
            if not data.get('itemsBlocks'):
                raise Exception('Interface in data is incorrect!')
            for block_key, block_structure in data['itemsBlocks'].items():
                print(block_key, block_structure)
                redis_client.set("block" + block_key, str(block_structure))
        else:
            raise Exception(f"Json file in path {initial_dump_path} doesn't exist")

    @property
    def redis(self, section: int = 0):
        return self._redis[section]

    def check_connection(self) -> None:
        self.redis.ping()

    def clear_cache_storage(self) -> None:
        for redis_section in self._redis.values():
            redis_section.flushall()

    def load_data_into_specific_part(self, key: str, value: str, section: int) -> None:
        self.redis.set(key, value)

    def load_start_cache(self) -> None:
        files = get_filenames_with_dump()
        for filename in files:
            with open(LOCAL_STORAGE_PATH + f'/{filename}') as f:
                data = json.load(f)
            for article in data:
                self.redis.set(article['url'], str(article))

    def load_cache(self, file_path: str, section: int = 0) -> None:
        redis_section = self._redis[section]
        if os.path.exists(file_path) and file_path.endswith('.json'):
            with open(file_path) as f:
                data = json.load(f)
            if isinstance(data, dict) and 'articles' in data:
                for article in data['articles']:
                    redis_section.set(article['url'], str(article))
                print(f'cache from file {file_path} is loaded!')
            if isinstance(data, list):
                for article in data:
                    redis_section.set(article['url'], str(article))
                print(f'cache from file {file_path} is loaded!')
        else:
            raise Exception(f"Json file in path {file_path} doesn't exist")

    def add_article_news_to_cache(self, articles: list[dict]) -> None:
        for article in articles:
            self.redis.hset(article['url'], mapping=article)

    def add_key_value(self, key: str, value: str) -> None:
        self.redis.set(key, value)

    def get_keys(self, section: int = 0) -> list[str]:
        return [key for key in self._redis[section].scan_iter()]

    def get_particular_values(self, key: str, section: int = 0) -> list[str]:
        """
        Returns list of values with key 'key' in structures.
        @param key:
        @param section:
        @return:
        """
        pass

    def find(self, search_term: str):
        search_results = []
        for section in self.available_sections:
            redis_section = self._redis[section]
            for key in redis_section.scan_iter():
                value = redis_section.get(key)
                if value and search_term in value:
                    search_results.append((key, value))
        return search_results

    async def get_actual_content(self):
        redis_section = self._redis[0]
        all_content_blocks = [key for key in redis_section.scan_iter()]
        for block_key in all_content_blocks:
            piece = redis_section.json().get(block_key)
            print(piece)


class CacheLoadQueryInterface:

    def __init__(self, search_query):
        self.query: str = search_query

    def get_string(self) -> str:
        return self.query


class CacheLoad(CacheSystem):
    loaders = [
        get_news_from_news_data_io,
        get_news_feed_everything
    ]

    def __init__(self):
        super().__init__()

    def load(self, query: CacheLoadQueryInterface):
        for section_to_load, loader in enumerate(self.loaders):
            file_path_from_loader = loader(query.get_string())
            self.load_cache(file_path=file_path_from_loader, section=section_to_load)


class Subject:
    pass


SubjectType = NewType('SubjectType', Subject)


class Article:
    url: str
    published_at: datetime.datetime
    title: str
    subject: SubjectType


def load_default_start_cache():
    cache_system = CacheSystem()
    default_dump_dir = '/home/skartavykh/MyProjects/media-bot/storage' + '/default_dump'
    for index, filename in enumerate(os.listdir(default_dump_dir)):
        file_path = os.path.join(default_dump_dir, filename)
        if os.path.isfile(file_path):
            db_section = index % REDIS_SECTIONS_COUNT
            cache_system.load_cache(file_path, db_section)


if __name__ == '__main__':
    cache_client = CacheSystem()
    asyncio.run(cache_client.get_actual_content())
