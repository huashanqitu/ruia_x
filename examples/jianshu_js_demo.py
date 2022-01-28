#!/usr/bin/env python
import sys
import os
root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)
from aspider import AttrField, TextField, Item, Spider


class JianshuItem(Item):
    target_item = TextField(css_select='ul.list>li')
    author_name = TextField(css_select='a.name')
    author_url = AttrField(attr='href', css_select='a.name')


class JianshuSpider(Spider):
    start_urls = ['https://www.jianshu.com/']
    concurrentcy = 10
    load_js = True

    async def parse(self, res):
        items = await JianshuItem.get_item(html=res.body)
        for item in items:
            print(item)


if __name__ == '__main__':
    JianshuSpider.start()