#!/usr/bin/env python


from aspider import Request, Spider

from items import HackerNewsItem
from middlewares import middleware


class HackerNewsSpider(Spider):
    start_urls = ["http://quibbler.cn/"]
    concurrency = 3

    async def parse(self, res):
        urls = ["http://quibbler.cn/?index-5.htm", "http://quibbler.cn/?index-6.htm"]
        for index, url in enumerate(urls):
            yield Request(
                url,
                callback=self.parse_item,
                metadata={'index': index}
            )

    async def parse_item(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            print(item.title)


if __name__ == '__main__':
    HackerNewsSpider.start(middleware=middleware)
