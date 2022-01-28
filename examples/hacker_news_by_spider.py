#!/usr/bin/env python
import sys
import os
root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)
import aiofiles

from aspider import AttrField, TextField, Spider, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='div.subject')
    title = TextField(css_select='a')
    links = AttrField(css_select='a', attr='href')

    async def clean_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])


class HackerNewsSpider(Spider):
    start_urls = ["http://quibbler.cn/?index-5.htm",
                  "http://quibbler.cn/?index-6.htm"]
    concurrency = 10

    async def parse(self, res):
        items = await HackerNewsItem.get_items(html=res.body)
        for item in items:
            async with aiofiles.open('./examples/hacker_news.txt', 'a+') as f:
                await f.write(item.title + '\n')


if __name__ == "__main__":
    HackerNewsSpider.start()
