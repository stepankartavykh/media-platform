import asyncio

import requests
import aiohttp

default_headers = requests.utils.default_headers()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
default_headers.update({'User-Agent': user_agent})


class RequestHandler:
    def __init__(self, url):
        self.url = url
        default_headers = requests.utils.default_headers()
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
        default_headers.update({'User-Agent': user_agent})
        self.headers = default_headers


async def make_async_request(url: str) -> asyncio.coroutines:
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=default_headers) as response:
            html = await response.text()
            return html


async def make_request_coroutine(url: str) -> str:
    return requests.get(url, headers=default_headers).text


def make_request(url: str) -> str:
    return requests.get(url, headers=default_headers).text


def get_status_code(url: str) -> int:
    try:
        response_first = requests.get(url)
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
        try:
            response_second = requests.get('https://' + url)
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            return -1
        else:
            return response_second.status_code
    else:
        return response_first.status_code


if __name__ == '__main__':
    obj = make_async_request('https://stackoveflow.com')
    asyncio.run(obj)
