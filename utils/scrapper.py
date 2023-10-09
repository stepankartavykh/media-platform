from utils import PageHandler


def start_processing(start_url):
    added_links = set()

    def run_process(incoming_url: str):
        handler = PageHandler(incoming_url)
        handler.get_all_links_from_page()
        for link in handler.links:
            if link not in added_links:
                added_links.add(link)
                print(link)
                run_process(link)

    run_process(start_url)
