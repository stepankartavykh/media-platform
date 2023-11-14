import asyncio
from typing import List

from utils import PageHandler
from telegram import Update


class StructuredMessage:
    pass


def form_message_for_bot(message):
    StructuredMessage()
    return "test message"


async def start_processing(sources: List[str], update: Update) -> None:
    added_links = set()

    async def run_process(incoming_url: str) -> None:
        handler = PageHandler(incoming_url)
        await handler.make_async_request()
        handler.get_all_links_from_page()
        message = handler.make_content_analysis()
        bot_message = form_message_for_bot(message)
        await update.message.reply_text(bot_message)
        for link in handler.links:
            if link not in added_links:
                added_links.add(link)
                await update.message.reply_text(f'{link}')
                await run_process(link)
    for source in sources:
        await run_process(source)


if __name__ == '__main__':
    asyncio.run(start_processing(['https://www.investopedia.com/']))
