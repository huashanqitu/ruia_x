#!/usr/bin/env python
import asyncio

from aspider import AttrField, TextField, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='div.subject')
    title = TextField(css_select='a')
    links = AttrField(css_select='a', attr='href')

    async def clean_title(self, value):
        return value


async_func = HackerNewsItem.get_items(url="http://quibbler.cn/?index-3.htm")
items = asyncio.get_event_loop().run_until_complete(async_func)
for item in items:
    print(item.title, item.links)
