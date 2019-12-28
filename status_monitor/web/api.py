from aiohttp import web
from pathlib import Path
import re


routes = web.RouteTableDef()

sample_projects = [
    { 'projectId': 'foo', 'name': 'Foo' },
    { 'projectId': 'bar', 'name': 'Bar' },
]


@routes.get('/api/projects')
async def index_handler(request):
    return web.json_response({
        'projects': sample_projects,
    })

