# TODO establish cache system functions. What are they?
"""
1. Insert data into cache. In what section you would insert entry? What the whole structure of Cache system?
2. Retrieve data from specific source.
3. Delete entry.
4. Update entry. Include functions to update by specific fields.
"""
import json

import redis
from config import REDIS_PORT, REDIS_HOST, LOCAL_STORAGE_PATH


def get_filenames_with_dump() -> list[str]:
    return ['bloomberg_quint_news.json']


class CacheSystem:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

    def check(self) -> None:
        self.redis.ping()

    def load_start_cache(self) -> None:
        files = get_filenames_with_dump()
        for filename in files:
            with open(LOCAL_STORAGE_PATH + f'/{filename}') as f:
                data = json.load(f)
            for article in data:
                self.redis.set(article['url'], str(article))

    def add_article_news_to_cache(self, articles: list[dict]) -> None:
        for article in articles:
            self.redis.hset(article['url'], mapping=article)
