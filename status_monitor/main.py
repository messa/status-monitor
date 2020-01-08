from argparse import ArgumentParser
from asyncio import get_running_loop, create_task
import asyncio
from aiohttp import web
from logging import getLogger
import os
from signal import SIGTERM
import sys

from .configuration import get_configuration
from .model import get_model
from .web.app import get_app


logger = getLogger(__name__)


def status_monitor_main():
    p = ArgumentParser()
    p.add_argument('--conf', metavar='FILE', help='path to configuration file')
    p.add_argument('--verbose', '-v', action='store_true')
    args = p.parse_args()
    setup_logging(verbose=args.verbose)
    cfg_path = args.conf or os.environ.get('CONF')
    if not cfg_path:
        sys.exit('Please provide configuration file path in --conf or CONF.')
    try:
        conf = get_configuration(cfg_path)
    except Exception as e:
        if type(e) is not Exception:
            logger.exception('Status monitor failed: %s', e)
        sys.exit(f'Failed to load configuration from {cfg_path}: {e}')
    if conf.log_file:
        setup_log_file(conf.log_file)
    try:
        logger.info('Status monitor starting')
        asyncio.run(async_main(conf))
        logger.info('Status monitor done')
    except BaseException as e:
        logger.exception('Status monitor failed: %s', e)
        sys.exit(f'ERROR: {e!r}')


log_format = '%(asctime)s %(name)-27s %(levelname)5s: %(message)s'


def setup_logging(verbose):
    from logging import DEBUG, ERROR, getLogger, Formatter, StreamHandler
    getLogger('').setLevel(DEBUG)
    h = StreamHandler()
    h.setFormatter(Formatter(log_format))
    h.setLevel(DEBUG if verbose else ERROR)
    getLogger('').addHandler(h)


def setup_log_file(log_file_path):
    from logging import DEBUG, getLogger, Formatter
    from logging.handlers import WatchedFileHandler
    h = WatchedFileHandler(str(log_file_path))
    h.setFormatter(Formatter(log_format))
    h.setLevel(DEBUG)
    getLogger('').addHandler(h)


async def async_main(conf):
    loop = get_running_loop()
    term_event = asyncio.Event()
    loop.add_signal_handler(SIGTERM, term_event.set)
    model = get_model(conf=conf)
    app = get_app()
    app['conf'] = conf
    app['model'] = model
    web_task = create_task(run_app(app, term_event))
    await web_task


async def run_app(app, stop_event):
    runner = web.AppRunner(app)
    try:
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()
        await stop_event.wait()
    finally:
        await runner.cleanup()
