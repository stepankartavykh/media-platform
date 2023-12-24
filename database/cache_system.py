import redis
from config import REDIS_PORT, REDIS_HOST


class CacheSystem:
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.redis = redis.Redis(host=host, port=port, decode_responses=True)

    def add_article_news_to_cache(self, articles: list[dict]) -> None:
        for article in articles:
            self.redis.hset(article['url'], mapping=article)
