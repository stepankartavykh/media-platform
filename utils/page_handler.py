"""Module to work with one page. Parse and make some necessary operations to analyse the content of the page."""
import json
import time

from bs4 import BeautifulSoup

from config import STORAGE_PATH, MAIN_DIR
from page_analyzer import Analyzer
from utils.system_utils import print_json_to_file
from .request_handler import make_async_request, make_request


class Topic:
    pass


def get_main_topics():
    return [
        'first topic',
        'second topic',
    ]


class StructuredPage:
    def __init__(self, content):
        self.content = content

    def form(self):
        struct = self.__parse_content()
        return struct
    
    def __parse_content(self):
        topics = get_main_topics()
        return {
            "topics": topics,
            "page_url": "test_url",
            "info": "test_info",
        }


class PageHandler:
    """Class to build page object to process coming page."""
    def __init__(self, page_url: str):
        """Initialize page. Get page source HTML code."""
        self.url = page_url
        self.links = []
        self.content = None
        self.structure = None

    async def make_async_request(self):
        self.content = await make_async_request(self.url)
        self.structure = StructuredPage(self.content).form()

    def make_request(self):
        self.content = make_request(self.url)
        self.structure = StructuredPage(self.content).form()

    def generate_file_path(self):
        url_ = self.url.replace('/', '')
        return MAIN_DIR + STORAGE_PATH + f'/{url_}{time.time()}'

    def write_page_source_code_to_file(self):
        path = self.generate_file_path()
        path = path + '.html'
        with open(path, 'w') as file_page:
            file_page.write(self.content)

    def get_all_links_from_page(self):
        """Get all available links on page. For next iteration of search."""
        soup = BeautifulSoup(self.content, features="html.parser")
        for link in soup.find_all('a'):
            link_str: str = link.get('href')
            if link_str and link_str != self.url and link_str.startswith('https://'):
                self.links.append(link.get('href'))

    def process_page_structure(self):
        analysis = Analyzer(self.structure)
        analysis.make_general_analysis()

    def make_content_analysis(self):
        print(self.links)
        soup = BeautifulSoup(self.content, features="html.parser")

        titles = [title.text.strip() for title in soup.select('.title-class')]
        descriptions = [desc.text.strip() for desc in soup.select('.description-class')]

        data = {
            'titles': titles,
            'descriptions': descriptions,
        }

        json_data = json.dumps(data)
        print_json_to_file(data)

        with open(MAIN_DIR + STORAGE_PATH + f'/parsed_data{time.time()}.json', 'w') as outfile:
            json.dump(data, outfile)
        return {}


def process_code():
    # TODO make StructuredPage class
    content = make_request('https://rbc.ru')
    structured_page = StructuredPage(content)
    struct = structured_page.form()
    print(struct)


if __name__ == '__main__':
    link = 'https://rbc.ru'
    for _ in range(10):
        handler = PageHandler(link)
        handler.make_request()
        handler.write_page_source_code_to_file()
        time.sleep(1)
