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
    user_id = request.match_info.get('id')
    async with request.app['db'].acquire() as conn:
        u = await db.get_user(conn, user_id=user_id)

    return web.json_response(u)


async def delete_user(request):
    user_id = request.match_info.get('id')
    async with request.app['db'].acquire() as conn:
        await db.delete_user(conn, user_id=user_id)

    return web.json_response({'id': user_id})


async def create_user(request: web.Request):
    data = await request.json()
    async with request.app['db'].acquire() as conn:
        user = await db.create_user(conn, username=data['name'], email=data['email'])
    return web.json_response(user)


async def update_user(request: web.Request):
    data = await request.json()
    user_id = data.pop('id')
    async with request.app['db'].acquire() as conn:
        res = await db.update_user(conn, user_id=user_id, **data)
    return web.json_response(res)


