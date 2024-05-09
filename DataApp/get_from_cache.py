import json
import redis

from config import LOCAL_STORAGE_PATH

cache_system = redis.Redis(host='localhost', port='6379', decode_responses=True)
cache_system.ping()


url = 'https://www.bloombergquint.com/markets/all-you-need-to-know-going-into-trade-on-september-23-2'


def get_data():
    return cache_system.get("https://www.bloombergquint.com/marke")


if __name__ == '__main__':
    data = get_data()
    print(data)
