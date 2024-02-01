# TODO establish cache system functions. What are they?
"""
1. Insert data into cache. In what section you would insert entry? What the whole structure of Cache system?
2. Retrieve data from specific source.
3. Delete entry.
4. Update entry. Include functions to update by specific fields.
"""


import redis
from config import REDIS_PORT, REDIS_HOST


class CacheSystem:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

    def add_article_news_to_cache(self, articles: list[dict]) -> None:
        for article in articles:
            self.redis.hset(article['url'], mapping=article)
