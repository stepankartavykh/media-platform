import time
from pathlib import Path
from typing import Any

import scrapy
from scrapy.http.response import Response

links = []


def get_path_to_save(file_name: str) -> str:
    return '/home/skartavykh/MyProjects/media-bot/storage/scrapydata/investopedia/' + file_name


class ExampleSpider(scrapy.Spider):
    name = "investopedia"
    allowed_domains = []
    # start_urls = ["https://www.investopedia.com"]

    def start_requests(self):
        urls = [
            "https://www.investopedia.com",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        print(response.url)
        # filename = get_path_to_save(response.url + '.html')
        # Path(filename).write_bytes(response.body)
        # self.log(f"Saved file {filename}")

        for link in response.css("a::attr(href)").getall():
            # print(link)
            # links.append(link)
            # if len(links) > 10:
            #     break
            # print(link)
            # time.sleep(2)
            yield response.follow(link, self.parse)
