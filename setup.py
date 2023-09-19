from setuptools import setup, find_packages

setup(
    name='mini-fastapi-gateway',
    version='0.0.1-beta-1',
    packages=find_packages(),
    url='',
    license='',
    author='aizhigito',
    author_email='aizhigit94@gmail.com',
    description='FastAPI gateway',
    download_url='https://github.com/aizhigito/fastapi-gateway/archive/refs/tags/v0.0.1-beta.tar.gz',
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
