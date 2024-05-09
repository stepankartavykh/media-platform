import json
from enum import Enum

import redis

from config import LOCAL_STORAGE_PATH

cache_system = redis.Redis(host='localhost', port='6379', decode_responses=True)
cache_system.ping()


class SuccessCode(Enum):
    ok = 1
    failure = 0


def load_cache_from_file(filename: str) -> list[dict]:
    with open(LOCAL_STORAGE_PATH + f'/{filename}') as f:
        data = json.load(f)
    return data


def send_data_to_cache_system(data: list[dict]) -> int:
    for article in data:
        cache_system.set(article['url'], str(article))
    return 1


if __name__ == '__main__':
    d = load_cache_from_file('bloomberg_quint_news.json')
    send_data_to_cache_system(d)
