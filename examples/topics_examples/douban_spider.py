from aspider import AttrField, TextField, Item, Request, Spider


class DoubanItem(Item):
    """
    定义爬虫的目标字段
    """

    target_item = TextField(css_select="div.item")
    title = TextField(css_select='span.title')
    cover = AttrField(css_select='div.pic>a>img', attr='src')
    abstract = TextField(css_select='span.inq')

    async def clean_title(self, title):
        if isinstance(title, str):
            return title
        else:
            return ''.join([i.text.strip().replace('\xa0', '') for i in title])


class DoubanSpider(Spider):
    """
    爬虫程序的入口
    """
    start_urls = ['https://movie.douban.com/top250']
    request_config = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 20
    }
    concurrency = 10

    async def parse(self, res):
        etree = res.e_html
        pages = ['?start=0&filter='] + [i.get('href') for i in etree.cssselect('.paginator>a')]
        for index, page in enumerate(pages):
            url = self.start_urls[0] + page
            yield Request(
                url,
                callback=self.parse_item,
                metadata={'index': index},
                request_config=self.request_config
            )

    async def parse_item(self, res):
        items_data = await DoubanItem.get_items(html=res.html)
        title_list = []
        for item in items_data:
            title_list.append(item.title)
        return title_list


if __name__ == '__main__':
    DoubanSpider.start()