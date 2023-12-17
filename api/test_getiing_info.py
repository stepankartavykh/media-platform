import json
from datetime import datetime

import requests

from config import STORAGE_PATH, NEWS_API_KEY, MAIN_DIR

url_everything = 'https://newsapi.org/v2/everything'
url_top_headlines = 'https://newsapi.org/v2/top-headlines'
sources_headlines = 'https://newsapi.org/v2/top-headlines'


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
    get_news_feed_everything('bitcoin')
