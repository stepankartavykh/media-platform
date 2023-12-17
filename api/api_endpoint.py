import json
from datetime import datetime

import requests
import aiohttp

from config import MAIN_DIR, STORAGE_PATH


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
            async with session.get(self.api_url, params=self.payload) as response:
                return await response.json()
