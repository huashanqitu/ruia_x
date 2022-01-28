#!/usr/bin/env python

import asyncio

from inspect import iscoroutinefunction

import aiohttp
import async_timeout
import cchardet
import pyppeteer

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

from aspider.response import Response
from aspider.utils import get_logger
from aspider.wrappers import SettingsWrapper


class Request():
    """
    Request class for each request
    """
    name = 'Request'

    # Default config
    REQUEST_CONFIG = {
        'RETRIES': 3,
        'DELAY': 0,
        'TIMEOUT': 10
    }

    METHOD = ['GET', 'POST']

    def __init__(self, url: str,
                 method: str = 'GET',
                 *,
                 callback=None,
                 load_js: bool = False,
                 metadata: dict = None,
                 extra_value: dict = None,
                 request_config: dict = None,
                 request_session=None,
                 res_type: str = 'text',
                 **kwargs):
        # TODO: cookie
        """
        Initialization parameters
        :param url:
        :param method:
        :param request_config:
        :param request_session:
        :param callback:
        :param extra_value:
        :param res_type:
        :param kwargs:
        """
        self.url = url
        self.method = method.upper()
        if self.method not in self.METHOD:
            raise ValueError('%s method is not supported' % self.method)

        self.callback = callback
        self.load_js = load_js
        self.metadata = metadata if metadata is not None else {}
        self.extra_value = extra_value if extra_value is not None else {}
        self.request_session = request_session
        if request_config is None:
            self.request_config = self.REQUEST_CONFIG
        else:
            self.request_config = request_config
        self.res_type = res_type
        self.kwargs = kwargs

        self.close_request_session = False
        self.logger = get_logger(name=self.name)
        self.retry_times = self.request_config.get('RETRIES', 3)
        # self.setting = SettingsWrapper()

    @property
    def current_request_func(self):
        self.logger.info(f"<{self.method}:{self.url}>")
        timeout = self.request_config.get('TIMEOUT', 10)
        if self.method == 'GET':
            request_func = self.current_request_session.get(self.url, verify_ssl=False, **self.kwargs)
        else:
            request_func = self.current_request_session.post(self.url, verify_ssl=False, **self.kwargs)
        return request_func

    @property
    def current_request_session(self):
        if self.request_session is None:
            self.request_session = aiohttp.ClientSession()
            self.close_request_session = True
        return self.request_session

    async def fetch(self) -> Response:
        if self.request_config.get('DELAY', 0) > 0:
            await asyncio.sleep(self.request_config['DELAY'])
        try:
            timeout = self.request_config.get('TIMEOUT', 10)
            if self.load_js:
                if not hasattr(self, "browser"):
                    self.browser = await pyppeteer.launch(headless=True, args=['--no-sandbox'])
                    page = await self.browser.newPage()
                    res = await page.goto(self.url, options={'timeout': int(timeout*1000)})
                    data = await page.content()
                    res_cookies = await page.cookies()
                    res_headers = res.headers
                    res_history = None
                    res_status = res.status
            else:
                async with async_timeout.timeout(timeout):
                    async with self.current_request_func as resp:
                        res_status = resp.status
                        assert resp.status in [200, 201]
                        if self.res_type == 'bytes':
                            data = await resp.read()
                        elif self.res_type == 'json':
                            data = await resp.json()
                        else:
                            content = await resp.read()
                            charset = cchardet.detect(content)
                            data = content.decode(charset['encoding'])
                        res_cookies, res_headers, res_history = resp.cookies, resp.headers, resp.history
        except Exception as e:
            res_headers = {}
            res_history = ()
            res_status = 0
            data, res_cookies = None, None
            self.logger.error(f"<Error:{self.url} {res_status} {str(e)}>")
        if self.retry_times > 0 and data is None:
            retry_times = self.request_config.get('RETRIES', 3) - self.retry_times + 1
            self.logger.info(f'<Retry url: {self.url}>, Retry times: {retry_times}')
            self.retry_times -= 1
            return await self.fetch()

        if self.close_request_session:
            await self.request_session.close()

        response = Response(url=self.url,
                            body=data,
                            metadata=self.metadata,
                            res_type=self.res_type,
                            cookies=res_cookies,
                            headers=res_headers,
                            history=res_history,
                            status=res_status)
        return response

    async def fetch_callback(self, sem):
        async with sem:
            res = await self.fetch()
        if self.callback is not None:
            try:
                if iscoroutinefunction(self.callback):
                    callback_res = await self.callback(res)
                else:
                    callback_res = self.callback(res)
            except Exception as e:
                self.logger.error(e)
                callback_res = None
        else:
            callback_res = None
        return callback_res, res

    def __str__(self):
        return "<%s %s>" % (self.method, self.url)