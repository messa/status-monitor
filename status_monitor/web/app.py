from aiohttp import web
from logging import getLogger
from pathlib import Path
import re

from .api import routes as api_routes
from .auth import routes as auth_routes
from .helpers import get_user


logger = getLogger(__name__)

routes = web.RouteTableDef()

here = Path(__file__).resolve().parent

static_frontend = here.parent.parent / 'frontend' / 'out'


@routes.get('/')
async def index_handler(request):
    user = await get_user(request)
    if not user:
        return web.HTTPFound(location='/login')
    else:
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



def get_app():
    app = web.Application()
    app.add_routes(routes)
    app.add_routes(api_routes)
    app.add_routes(auth_routes)

    next_static_dir = static_frontend / '_next'
    if next_static_dir.exists():
        app.add_routes([
            web.static('/_next', next_static_dir),
        ])
    else:
        logger.warning('Next.js static dir does not exist: %s', next_static_dir)


    return app
