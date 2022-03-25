#!/usr/bin/env python
import aiofiles

from aspider import AttrField, TextField, Item, Spider


class HackerNewsItem(Item):
    target_item = TextField(css_select='div.subject')
    title = TextField(css_select='a')
    links = AttrField(css_select='a', attr='href')

    async def clean_title(self, value):
        return value


class HackerNewsSpider(Spider):
    start_urls = ["http://quibbler.cn/?index-5.htm",
                  "http://quibbler.cn/?index-6.htm"]
    concurrency = 10

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.html)
        for item in items:
            async with aiofiles.open('./hacker_news.txt', 'a+') as f:
                await f.write(item.title + '\n')


if __name__ == '__main__':
    HackerNewsSpider.start(middleware=None)
