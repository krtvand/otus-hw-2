from os import environ

from aiopg.sa import SAConnection
from sqlalchemy import (
    MetaData,
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    create_engine,
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
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(64), nullable=False, unique=True),
    Column('email', String(120)),
)


async def get_user(conn, user_id):
    records = await conn.execute(users.select().where(users.c.id == user_id))
    r = await records.first()
    return {'id': r[0], 'name': r[1], 'email': r[2]}


async def get_users(conn):
    cursor = await conn.execute(users.select().order_by(users.c.id))
    rows = await cursor.fetchall()

    return [{'id': r[0], 'name': r[1], 'email': r[2]} for r in rows]


async def create_user(conn, username, email):
    stmt = (
        users.insert()
        .values(username=username, email=email)
        .returning(users.c.id)
    )
    response = await conn.execute(stmt)
    result = await response.fetchone()

    return {'id': result[0], 'name': username, 'email': email}


async def update_user(conn, user_id, **params):
    res = await conn.execute(
        users
        .update()
        .where(users.c.id == user_id)
        .returning(*users.c)
        .values(**params)
    )
    record = await res.fetchone()
    if not record:
        msg = "User does not exists"
        raise RecordNotFound(msg)
    return {'id': record[0], 'name': record[1], 'email': record[2]}


async def delete_user(conn, user_id):
    await conn.execute(
        users
        .delete()
        .where(users.c.id == user_id)
    )


class RecordNotFound(Exception):
    pass
