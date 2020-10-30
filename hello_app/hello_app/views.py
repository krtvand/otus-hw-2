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

async def create_user(request: web.Request):
    data = await request.json()
    async with request.app['db_pool'].acquire() as conn:
        user = await db.create_user(conn, username=data['name'], email=data['email'])
    return web.json_response({'name': data['name'], 'id': 1})

