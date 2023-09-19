from setuptools import setup, find_packages

setup(
    name='fastapi-gateway',
    version='0.0.1',
    packages=find_packages(),
    url='',
    license='',
    author='aizhigito',
    author_email='aizhigit94@gmail.com',
    description='FastAPI gateway',
    install_requires=[
        'fastapi',
        'sqlalchemy',
        'alembic',
        'pydantic_settings',
        'aiohttp',
        'cachetools',
        'ujson'
    ],
    extras_require={},
    entry_points={
        'console_scripts': [
            'gateway = app.main:main'
        ]
    }
)