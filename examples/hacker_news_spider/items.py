#!/usr/bin/env python


from aspider import AttrField, TextField, Item


class HackerNewsItem(Item):
    target_item = TextField(css_select='div.subject')
    title = TextField(css_select='a')
    links = AttrField(css_select='a', attr='href')

    async def clean_title(self, value):
        return value
