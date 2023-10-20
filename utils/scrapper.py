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
