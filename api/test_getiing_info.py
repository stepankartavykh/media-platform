import json
from datetime import datetime

import requests

from config import STORAGE_PATH, NEWS_API_KEY, MAIN_DIR, NEWS_DATA_IO_KEY

url_everything = 'https://newsapi.org/v2/everything'
url_top_headlines = 'https://newsapi.org/v2/top-headlines'
sources_headlines = 'https://newsapi.org/v2/top-headlines'

url_news_io = 'https://newsdata.io/api/1/news'


def get_news_from_news_data_io(topic: str):
    payload = {
        'q': topic,
        'apikey': NEWS_DATA_IO_KEY,
        'language': 'ru',
    }
    response = requests.get(url_news_io, params=payload)
    template = '%Y-%m-%d_%H-%M-%S'
    path_to_save = MAIN_DIR + STORAGE_PATH + f'/{datetime.now().strftime(template)}_news_data.io.json'
    with open(path_to_save, 'w') as f:
        json.dump(response.json(), f, indent=4)


def get_news_feed_everything(topic: str):
    everything_payload = {
        'q': topic,
        'apiKey': NEWS_API_KEY,
    }
    response = requests.get(url_everything, params=everything_payload)
    template = '%Y-%m-%d_%H-%M-%S'
    path_to_save = MAIN_DIR + STORAGE_PATH + f'/{datetime.now().strftime(template)}_everything_feed.json'
    with open(path_to_save, 'w') as f:
        json.dump(response.json(), f, indent=4)


if __name__ == '__main__':
    query = input()
    get_news_feed_everything(query)
    get_news_from_news_data_io(query)
