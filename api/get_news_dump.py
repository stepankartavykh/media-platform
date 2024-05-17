import json
from datetime import datetime
from enum import Enum

import requests

from api.config import NEWS_API_KEY, MAIN_DIR, NEWS_DATA_IO_KEY, STORAGE_PATH

url_everything = 'https://newsapi.org/v2/everything'
url_top_headlines = 'https://newsapi.org/v2/top-headlines'
sources_headlines = 'https://newsapi.org/v2/top-headlines'

url_news_io = 'https://newsdata.io/api/1/news'


class SearchInOptions(Enum):
    title = "title"
    description = "description"
    content = "content"


class NewsAPIErrorLoad(Exception):
    message = "Error with getting info from newsapi.org"


def get_news_from_news_data_io(topic: str) -> str:
    payload = {
        'q': topic,
        'apikey': NEWS_DATA_IO_KEY,
        'language': 'en',
    }
    response = requests.get(url_news_io, params=payload)
    template = '%Y-%m-%d_%H-%M-%S'
    path_to_save = MAIN_DIR + STORAGE_PATH + f'/{datetime.now().strftime(template)}_news_data.io.json'
    with open(path_to_save, 'w') as f:
        json.dump(response.json(), f, indent=4, ensure_ascii=False)
    return path_to_save


def get_news_feed_everything(topic: str,
                             search_in: str = None,
                             sources: str = None,
                             domains: str = None,
                             exclude_domains: str = None,
                             from_: str = None,
                             to: str = None,
                             lang: str = None,
                             sort_by: str = None,
                             page_size: int = None,
                             page: int = None) -> str:
    if not NEWS_API_KEY:
        raise Exception('There is no NEWS_API_KEY in .env')
    everything_payload = {
        'q': topic,
        'apiKey': NEWS_API_KEY,
    }
    if search_in:
        everything_payload['searchIn'] = search_in
    if sources:
        everything_payload['sources'] = sources
    if domains:
        everything_payload['domains'] = domains
    if exclude_domains:
        everything_payload['excludeDomains'] = exclude_domains
    if from_:
        everything_payload['from'] = from_
    if to:
        everything_payload['to'] = to
    if lang:
        everything_payload['language'] = lang
    if sort_by:
        everything_payload['sortBy'] = sort_by
    if page_size:
        everything_payload['pageSize'] = page_size
    if page:
        everything_payload['page'] = page
    response = requests.get(url_everything, params=everything_payload)
    if response.json().get('status') != 'ok':
        print('Error with query to API!')
        raise NewsAPIErrorLoad(f'error with loading data via {response.url}')
    template = '%Y-%m-%d_%H-%M-%S-%f'
    path_to_save = MAIN_DIR + STORAGE_PATH + f'/{datetime.now().strftime(template)}_everything_feed.json'
    with open(path_to_save, 'w') as f:
        json.dump(response.json(), f, indent=4)
    return path_to_save


if __name__ == '__main__':
    query = input()
    print(get_news_feed_everything(query))
    print(get_news_from_news_data_io(query))
