import logging
from os import environ

from aiohttp import web

from hello_app import db
from hello_app.db import init_db


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def health(request):
    return web.Response(text='{"status": "OK"}')


async def liveness(request):
    return web.Response(text='{"status": "OK"}')


async def readiness(request):
    return web.Response(text='{"status": "OK"}')


async def get_user_list(request):

    async with request.app['db_pool'].acquire() as conn:
        users = await db.get_users(conn)

    result = []
    for u in users:
        result.append({'id': u['id']})

    return web.json_response(result)


async def get_user(request):
    name = request.match_info.get('name')
    text = "Hello, " + name

    return web.json_response({'name': '', 'id': 1})


FLASK_ENV = environ.get('FLASK_ENV')


def load_config():
    conf = {}
    db_conf = dict(
        DB_USER=environ.get('DB_USER', 'otus-hw'),
        DB_PASS=environ.get('DB_PASS', 'otus-hw'),
        DB_NAME=environ.get('DB_NAME', 'otus-hw'),
        DB_HOST=environ.get('DB_HOST', 'otus-hw'),
        DB_PORT=int(environ.get('DB_PORT', 30001))
    )
    conf['database'] = db_conf

    return conf


def setup_routes(app):
    app.add_routes(
        [
            web.get('/', handle),
            web.get('/health', health),
            web.get('/liveness', liveness),
            web.get('/readiness', readiness),
            web.get('/user', get_user_list),
            web.get('/user/{name}', get_user),
        ]
    )


async def init_app(config):

    app = web.Application()

    app['config'] = config

    setup_routes(app)

    await init_db(app)

    return app


app = web.Application()


def main():
    logging.basicConfig(level=logging.DEBUG)
    config = load_config()
    app = init_app(config)
    web.run_app(
        app,
        host=environ.get('HOST', '0.0.0.0'),
        port=int(environ.get('PORT', 8000)),
    )


if __name__ == '__main__':
    main()
