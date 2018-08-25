from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/')
async def index(request):
    return web.Response(text="Hello, World!")


def setup_routes(app):
    app.router.add_get('/', index)


def main():
    app = web.Application()
    setup_routes(app)
    web.run_app(app)
