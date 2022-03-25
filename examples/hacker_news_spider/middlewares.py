#!/usr/bin/env python


from aspider import Middleware

middleware = Middleware()


@middleware.request
async def print_on_request(request):
    ua = 'aspider user-agent'
    request.headers.update({'User-Agent': ua})
