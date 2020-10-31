from os import environ

import asyncpgsa
from aiopg.sa import SAConnection
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime, create_engine
)
import aiopg.sa
from sqlalchemy.sql import select
from sqlalchemy.sql.ddl import CreateTable

metadata = MetaData()


async def init_db(app):
    config = app['config']['database']
    engine = await aiopg.sa.create_engine(
        database=config['DB_NAME'],
        user=config['DB_USER'],
        password=config['DB_PASS'],
        host=config['DB_HOST'],
        port=config['DB_PORT'],
    )
    app['db'] = engine

    # create_tables
    return engine


async def create_tables(conn: SAConnection) -> None:
    await conn.execute(CreateTable(users))


def construct_db_url(config):
    DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"
    return DSN.format(
        user=config['DB_USER'],
        password=config['DB_PASS'],
        database=config['DB_NAME'],
        host=config['DB_HOST'],
        port=config['DB_PORT'],
    )



users = Table(
    'users', metadata,

    Column('id', Integer, primary_key=True),
    Column('username', String(64), nullable=False, unique=True),
    Column('email', String(120)),
)


async def get_users(conn):
    records = await conn.fetch(
        users.select().order_by(users.c.id)
    )
    return records


async def create_user(conn, username, email):
    stmt = users.insert().values(username=username, email=email).returning(users.c.id)
    response = await conn.execute(stmt)
    result = await response.fetchone()

    return {'id': result[0], 'name': username, 'email': email}


async def update_user(conn, params):
    res = await conn.execute(
        users.update()
        .returning(*users.c)
        .values(params)
    )
    record = await res.fetchone()
    if not record:
        msg = "Question does not exists"
        raise RecordNotFound(msg)


class RecordNotFound(Exception):
    pass