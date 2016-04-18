# -*- coding: utf-8 -*-
import asyncio
import logging

from aiohttp import web
from aiohttp_auth import auth
from aiohttp_session import get_session, session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from ircb.config import settings
from ircb.web.user import SigninView, SignoutView, SignupView
from ircb.web.network import NetworkListView, NetworkView
from ircb.web.network import NetworkConnectionView
from ircb.utils.config import load_config

logger = logging.getLogger(__name__)


@asyncio.coroutine
def index(request):
    return web.Response(body=b"Hello, ircb!")


@asyncio.coroutine
def init(loop):
    from ircb.storeclient import initialize
    initialize()
    load_config()
    policy = auth.SessionTktAuthentication(
        settings.WEB_SALT, 60, include_ip=True)
    middlewares = [
        session_middleware(EncryptedCookieStorage(settings.WEB_SALT)),
        auth.auth_middleware(policy)
    ]

    app = web.Application(middlewares=middlewares)
    app.router.add_route('GET', '/', index)

    app.router.add_route('*', '/api/v1/signup', SignupView, name='signup')
    app.router.add_route('*', '/api/v1/signin', SigninView, name='signin')
    app.router.add_route('*', '/api/v1/signout', SignoutView, name='signout')
    app.router.add_route('*', '/api/v1/networks', NetworkListView,
                         name='networks')
    app.router.add_route('*', '/api/v1/network/{id}', NetworkView,
                         name='network')
    app.router.add_route('PUT', '/api/v1/network/{id}/{action}',
                         NetworkConnectionView,
                         name='network_connection')
    srv = yield from loop.create_server(
        app.make_handler(logger=logger, access_log=logger), '0.0.0.0', 10001)
    return srv

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
