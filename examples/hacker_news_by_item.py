#!/usr/bin/env python
import asyncio

from pprint import pprint

from aspider import AttrField, Item, TextField


class HackerNewsItem(Item):
    target_item = TextField(css_select='div.subject')
    title = TextField(css_select='a')
    links = AttrField(css_select='a', attr='href')

    async def clean_title(self, title):
        # return title
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])


async_func = HackerNewsItem.get_items(url="http://quibbler.cn/?index-3.htm")
items = asyncio.get_event_loop().run_until_complete(async_func)
for item in items:
    print(item.title, item.links)
