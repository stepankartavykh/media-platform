import asyncio
from typing import List

from utils import PageHandler
from telegram import Update


class StructuredMessage:
    pass


def form_message_for_bot(message):
    StructuredMessage()
    return "test message"


async def start_async_processing(sources: List[str], update: Update) -> None:
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


def start_processing(link) -> None:
    visited_links = set()

    def run_process(incoming_url: str) -> None:
        handler = PageHandler(incoming_url)
        handler.make_request()
        handler.get_all_links_from_page()
        handler.write_page_source_code_to_file()
        structured_content = handler.make_content_analysis()
        for internal_link in handler.links:
            if internal_link not in visited_links:
                visited_links.add(link)
                run_process(link)

    run_process(link)


if __name__ == '__main__':
    links = [
        'https://www.kommersant.ru/',
        'https://www.rbc.ru/',
    ]
    start_processing(links[0])
