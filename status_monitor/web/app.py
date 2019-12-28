from aiohttp import web


routes = web.RouteTableDef()


@routes.get('/')
async def hello(request):
    return web.Response(text="Hello, world")


def get_app():
    app = web.Application()
    app.add_routes(routes)
    return app
