import logging
from os import environ

from aiohttp import web

from hello_app import db
from hello_app.db import init_db
from hello_app import views



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
            web.get('/', views.handle),
            web.get('/health', views.health),
            web.get('/liveness', views.liveness),
            web.get('/readiness', views.readiness),
            web.get('/user', views.get_user_list),
            web.get('/user/{id}', views.get_user),
            web.post('/user', views.create_user),
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
