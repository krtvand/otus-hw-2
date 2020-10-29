from setuptools import setup


install_requires = [
    'aiohttp',
    'aiohttp-jinja2',
    'bcrypt',
    'pytoml',
    'aiohttp_security[session]',
    'sqlalchemy',
    'asyncpg',
    'asyncpgsa',
    'psycopg2',
]

setup(
    name='hello_app',
    version='0.1.0',
    packages=['hello_app'],
    entry_points={'console_scripts': ['hello_app = hello_app.main:main']},
    url='',
    license='',
    author='Andrey Kartaev',
    author_email='a.kartaev@qrator.net',
    description='',
    install_requires=install_requires,
)
