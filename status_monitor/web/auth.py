from aiohttp import web
from pathlib import Path
import re


routes = web.RouteTableDef()


@routes.get('/api/auth/google')
async def index_handler(request):
    return web.json_response({
    })

@routes.get('/api/auth/google-callback')
async def index_handler(request):
    return web.json_response({
    })

