## aspider

[![travis](https://travis-ci.org/howie6879/aspider.svg?branch=master)](https://travis-ci.org/howie6879/aspider) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aspider.svg)](https://pypi.org/project/aspider/) [![license](https://img.shields.io/github/license/howie6879/aspider.svg)](https://github.com/howie6879/aspider)

A lightweight,asynchronous micro-framework, written with `asyncio` and `aiohttp`, aims to make crawling url as convenient as possible.


### Installation
``` shell
pip install git+https://github.com/huashanqitu/aspider
```
### Usage

#### Request & Response
We provide an easy way to `request` a url and return a friendly `response`:

**JavaScript Support**
``` python
request = Request("https://www.jianshu.com/", load_js=True)
response = asyncio.get_event_loop().run_until_complete(request.fetch())
print(response.body)
```

Note, when you ever run the `fetch()` method first time,, it will download a recent version of Chromium(~100MB). This only happens once.

#### Item

Let's take a look at a quick example of using `Item` to extract target data. Start off by adding the following to your demo.py:

```
```

Run: `python demo.py`

``` 
```

#### Spider

For multiple pages, you can solve this with `Spider`

Create `hacker_news_spider.py`


### License
aspider is offered under the MIT license.

### TODO

- [ ] Custom middleware
- [x] Friendly response

### Contribution

- Pull Request
- Open Issue

### Thanks

- [demiurge](https://github.com/matiasb/demiurge)