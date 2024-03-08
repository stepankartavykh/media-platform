import json
import datetime
import requests
import aiohttp

from config import MAIN_DIR, STORAGE_PATH


class ApiEndpoint:
    def __init__(self, url, payload, api_type, interface):
        self.api_url = url
        self.payload = payload
        self.api_type = api_type
        self.interface = interface

    def get_api_response(self) -> dict:
        response = requests.get(self.api_url, params=self.payload)
        return response.json()

    def save_api_response_to_path(self):
        response = self.get_api_response()
        template = '%Y-%m-%d_%H-%M-%S'
        path_to_save = MAIN_DIR + STORAGE_PATH + f'/{datetime.datetime.now().strftime(template)}_{self.api_type}.json'
        with open(path_to_save, 'w') as f:
            json.dump(response, f, indent=4)

    async def get_api_async_response(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.api_url, params=self.payload) as response:
                return await response.json()


class Source:
    def __init__(self, url=None):
        self.base_url = url

    def get_content(self):
        return requests.get(self.base_url).text


sources = [
    Source('https://kommersant.ru'),
    Source('https://rbc.ru'),
    Source('https://ria.ru'),
    Source('https://tass.ru'),
    Source('https://rg.ru'),
    Source('https://russian.rt.com'),
]


def add_article_to_cache(article_json, interface):
    """Function to send article content to cache system according to interface of source API"""
    pass


if __name__ == '__main__':
    for source in sources:
        print(source.get_content())
