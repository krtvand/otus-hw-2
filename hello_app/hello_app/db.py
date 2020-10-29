from os import environ

import asyncpgsa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime
)
from sqlalchemy.sql import select

metadata = MetaData()


async def init_db(app):
    dsn = construct_db_url(app['config']['database'])
    pool = await asyncpgsa.create_pool(dsn=dsn)
    # engine = create_engine(dsn)
    # metadata.create_all(bind=engine, tables=[users])
    app['db_pool'] = pool
    return pool


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
    Column('password_hash', String(128), nullable=False)
)


async def get_users(conn):
    records = await conn.fetch(
        users.select().order_by(users.c.id)
    )
    return records



async def create_user(conn, username, email):
    stmt = users.insert().values(username=username, email=email)
    await conn.execute(stmt)