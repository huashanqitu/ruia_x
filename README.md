## aspider

[![travis](https://travis-ci.org/howie6879/aspider.svg?branch=master)](https://travis-ci.org/howie6879/aspider) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aspider.svg)](https://pypi.org/project/aspider/) [![license](https://img.shields.io/github/license/howie6879/aspider.svg)](https://github.com/howie6879/aspider)

An async web scraping micro-framework, written with `asyncio` and `aiohttp`, aims to make crawling url as convenient as possible.

### Installation
``` shell
# For Linux & Mac
pip install -U aspider[uvloop]

# For Windows
pip install -U aspider

# New features
pip install git+https://github.com/howie6879/aspider
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

#### Custom middleware

`aspider` provides an easy way to customize requests, *as long as it does not return it*. 

The following middleware code is based on the above example:

``` python
from aspider import Middleware

middleware = Middleware()


@middleware.request
async def print_on_request(request):
    request.metadata = {
        'index': request.url.split('=')[-1]
    }
    print(f"request: {request.metadata}")


@middleware.response
async def print_on_response(request, response):
    print(f"response: {response.metadata}")

# Add HackerNewsSpider

if __name__ == '__main__':
    HackerNewsSpider.start(middleware=middleware)
```

#### Extensions

A list of aspider extensions created by the community:

- [aspider-ua](https://github.com/howie6879/aspider-ua)

### TODO

- [x] Custom middleware
- [x] JavaScript support
- [x] Friendly response

### Contribution

- Pull Request
- Open Issue

### Thanks

- [demiurge](https://github.com/matiasb/demiurge)