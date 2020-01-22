from argparse import ArgumentParser
from asyncio import FIRST_EXCEPTION, get_running_loop, create_task, wait
import asyncio
from aiohttp import web
from logging import getLogger
import os
from signal import SIGTERM
import sys

from .check_processing import run_monitoring
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


log_format = '%(asctime)s %(name)-43s %(levelname)5s: %(message)s'


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
    web_app = get_app()
    web_app['conf'] = conf
    web_app['model'] = model
    tasks = []
    try:
        tasks.append(create_task(run_app(web_app, term_event)))
        tasks.append(create_task(run_monitoring(conf, model, term_event)))
        done, pending = await wait(tasks, return_when=FIRST_EXCEPTION)
        for task in done:
            try:
                await task
            except Exception as e:
                logger.debug('Main task %s finished with exception: %r', task, e)

    finally:
        to_cancel = [t for t in tasks if not t.done()]
        for task in to_cancel:
            logger.debug('Cancelling main task %r', task)
            task.cancel()
        for task in to_cancel:
            try:
                await task
            except Exception as e:
                logger.debug('Main task %s finished with exception after cancel: %r', task, e)


async def run_app(app, stop_event):
    runner = web.AppRunner(app)
    try:
        await runner.setup()
        site = web.TCPSite(runner, 'localhost', 8080)
        await site.start()
        await stop_event.wait()
    finally:
        await runner.cleanup()


