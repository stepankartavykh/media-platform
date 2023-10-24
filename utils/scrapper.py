import asyncio
from typing import List

from utils import PageHandler
from telegram import Update


async def start_processing(sources: List[str], update: Update) -> None:
    added_links = set()

    async def run_process(incoming_url: str) -> None:
        handler = PageHandler(incoming_url)
        await handler.make_request()
        handler.get_all_links_from_page()
        for link in handler.links:
            if link not in added_links:
                added_links.add(link)
                await update.message.reply_text(f'{link}')
                await run_process(link)
    for source in sources:
        await run_process(source)


if __name__ == '__main__':
    asyncio.run(start_processing(['https://www.investopedia.com/']))
