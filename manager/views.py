from aiohttp import web


async def index(app):
    return web.Response(text="Hello there!")
