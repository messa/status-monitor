from aiohttp import web
from pathlib import Path
import re

from .api import routes as api_routes
from .auth import routes as auth_routes


routes = web.RouteTableDef()

here = Path(__file__).resolve().parent

static_frontend = here.parent.parent / 'frontend' / 'out'


@routes.get('/')
async def index_handler(request):
    return web.HTTPFound(location='/dashboard')


@routes.get('/{filename}')
async def static_html_handler(request):
    filename = request.match_info['filename']
    if re.match(r'^[a-z]+$', filename):
        full_path = static_frontend / (filename + '.html')
        if full_path.is_file():
            return web.Response(
                body=full_path.read_bytes(),
                content_type='text/html')
    return web.Response(status=404, text='Page not found\n')


routes.static('/_next', static_frontend / '_next')


def get_app():
    app = web.Application()
    app.add_routes(routes)
    app.add_routes(api_routes)
    return app
