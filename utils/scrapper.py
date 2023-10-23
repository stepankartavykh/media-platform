import asyncio
from typing import List

from utils import PageHandler


async def start_processing(sources: List[str]) -> None:
    added_links = set()

    async def run_process(incoming_url: str) -> None:
        handler = PageHandler(incoming_url)
        handler.get_all_links_from_page()
        for link in handler.links:
            if link not in added_links:
                added_links.add(link)
                print(link)
                await run_process(link)
    for source in sources:
        await run_process(source)


if __name__ == '__main__':
    # task = asyncio.create_task(start_processing(['https://www.kommersant.ru/']))
    asyncio.run(start_processing(['https://www.kommersant.ru/']))


async def my_coroutine():
    # do something async
    await asyncio.sleep(2)
    print("Welcome to Sling Academy!")


async def main():
    loop = asyncio.get_event_loop()
    if loop.is_running():
        print(f"Event loop is already running.")
    future = asyncio.ensure_future(my_coroutine())
    await future
