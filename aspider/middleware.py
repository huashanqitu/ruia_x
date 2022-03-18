#! /usr/bin/env python

from collections import deque
from functools import wraps


class Middleware:
    """
    Define a middleware to customize the crawler request_test or response
    eg: middleware = Middleware()
    """

    def __init__(self):
        # request_test middleware
        self.request_middleware = deque()
        # response middleware
        self.response_middleware = deque()

    def listener(self, uri, target, **kwargs):
        """
        Decorates to be called before a special request_test or response
        TODO: handling different urls for request_test/response
        eg: @middleware.listener('/post', 'request_test')
        """

        def register_middleware(middleware):
            if target == 'request_test':
                self.request_middleware.append(middleware)
            if target == 'response':
                self.response_middleware.append(middleware)
            return middleware

        return register_middleware

    def request(self, *args, **kwargs):
        """
        Define a Decorate to be called before a request_test.
        eg: @middleware.request_test
        """
        middleware = args[0]

        @wraps(middleware)
        def register_middleware(*args, **kwargs):
            self.request_middleware.append(middleware)
            return middleware

        return register_middleware()

    def response(self, *args, **kwargs):
        """
        Define a Decorate to be called after a response.
        eg: @middleware.response
        """
        middleware = args[0]

        @wraps(middleware)
        def register_middleware(*args, **kwargs):
            self.response_middleware.appendleft(middleware)
            return middleware

        return register_middleware()