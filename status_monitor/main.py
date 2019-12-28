from argparse import ArgumentParser
import asyncio
from aiohttp import web

from .web.app import get_app


def status_monitor_main():
    p = ArgumentParser()
    args = p.parse_args()
    print('Status monitor starting')
    asyncio.run(async_main())


async def async_main():
    app = get_app()
    runner = web.AppRunner(app)
    try:
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()
        while True:
            await asyncio.sleep(10)
    finally:
        await runner.cleanup()
