import json
from datetime import datetime

import aiohttp
import requests

from config import STORAGE_PATH, NEWS_API_KEY, MAIN_DIR
from utils.request_handler import default_headers

url_everything = 'https://newsapi.org/v2/everything'
url_top_headlines = 'https://newsapi.org/v2/top-headlines'
sources_headlines = 'https://newsapi.org/v2/top-headlines'


class ApiEndpoint:
    def __init__(self, url, payload, api_type):
        self.api_url = url
        self.payload = payload
        self.api_type = api_type

    def get_api_response(self) -> dict:
        response = requests.get(self.api_url, params=self.payload)
        return response.json()

    def save_api_response_to_path(self):
        response = self.get_api_response()
        template = '%Y-%m-%d_%H-%M-%S'
        path_to_save = MAIN_DIR + STORAGE_PATH + f'/{datetime.now().strftime(template)}_{self.api_type}.json'
        with open(path_to_save, 'w') as f:
            json.dump(response, f, indent=4)

    async def get_api_async_response(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url, headers=self.payload) as response:
                return await response.json()


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


# def get_news_feed_top_headlines(topic: str):
#     top_headlines_payload = {
#         'q': topic,
#         'apiKey': NEWS_API_KEY,
#     }
#     response = requests.get(url_top_headlines, params=top_headlines_payload)
#     template = '%Y-%m-%d_%H-%M-%S'
#     path_to_save = MAIN_DIR + STORAGE_PATH + f'/{datetime.now().strftime(template)}_top_headlines.json'
#     with open(path_to_save, 'w') as f:
#         json.dump(response.json(), f, indent=4)
#
#
# def get_news_feed_top_headlines(topic: str):
#     top_headlines_payload = {
#         'q': topic,
#         'apiKey': NEWS_API_KEY,
#     }
#     response = requests.get(url_top_headlines, params=top_headlines_payload)
#     template = '%Y-%m-%d_%H-%M-%S'
#     path_to_save = MAIN_DIR + STORAGE_PATH + f'/{datetime.now().strftime(template)}_top_headlines.json'
#     with open(path_to_save, 'w') as f:
#         json.dump(response.json(), f, indent=4)


if __name__ == '__main__':
    everything_payload = {
        'q': 'war',
        'apiKey': NEWS_API_KEY,
    }
    everything_endpoint = ApiEndpoint(url_everything, everything_payload, 'everything_on_topic')
    print(everything_endpoint.get_api_response())

    get_news_feed_everything('chatgpt')