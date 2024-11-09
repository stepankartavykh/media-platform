from typing import Iterable, Any

import scrapy
from scrapy.http import Request, Response


class SecondSpider(scrapy.Spider):
    name = "second"
    allowed_domains = ["cnbc.com"]
    start_urls = ["https://cnbc.com"]

    def start_requests(self) -> Iterable[Request]:
        urls = self.start_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        print(response.body)
        # if response.status == 403:
        #     print(response.__dict__)
        #     raise
