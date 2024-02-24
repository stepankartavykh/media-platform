import datetime
import json
from typing import Optional

import requests
from pydantic import BaseModel, Field

from config import NEWS_API_KEY, MAIN_DIR, STORAGE_PATH


class SourceInterface(BaseModel):
    id: Optional[str]
    name: str


class ArticleInterface(BaseModel):
    source: SourceInterface
    author: Optional[str]
    title: str
    description: Optional[str]
    url: str
    url_to_image: Optional[str] = Field(alias='urlToImage')
    published_at: datetime.datetime = Field(alias='publishedAt')


class EverythingResponseInterface(BaseModel):
    status: str
    total_results: int = Field(alias='totalResults')
    articles: list[ArticleInterface]


class Source:
    def __init__(self, url, api_key, params):
        self.base_url = url
        self.api_key = api_key
        self.request_params = params


def dump_response_to_file(response: requests.Response):
    template = '%Y-%m-%d_%H-%M-%S'
    path_to_save = MAIN_DIR + STORAGE_PATH + f'/{datetime.datetime.now().strftime(template)}_everything_feed.json'
    with open(path_to_save, 'w') as f:
        json.dump(response.json(), f, indent=4)


def get_news_feed_everything(topic: str):
    everything_payload = {
        'q': topic,
        'apiKey': NEWS_API_KEY,
    }
    url_everything = 'https://newsapi.org/v2/everything'
    response = requests.get(url_everything, params=everything_payload)
    dump_response_to_file(response)
    everything_on_topic = EverythingResponseInterface.model_validate_json(response.text)
    for article in everything_on_topic.articles[:15]:
        print(article.published_at)


def get_dates_from_response():
    with open(MAIN_DIR + STORAGE_PATH + '/test_dump.json') as f:
        dump = json.load(f)
    everything_on_topic = EverythingResponseInterface.model_validate(dump)
    for article in everything_on_topic.articles[:15]:
        print(article.published_at)


if __name__ == '__main__':
    t = 'economics'
    # get_news_feed_everything(t)
    get_dates_from_response()
