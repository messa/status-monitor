from asyncio import CancelledError, TimeoutError, Event, create_task, sleep, wait, FIRST_COMPLETED
from logging import getLogger


logger = getLogger(__name__)


reload_interval_s = 30
shutdown_wait_s = 3


async def run_monitoring(conf, model, stop_event):
    conf_version = conf.get_reload_version()
    mon_task = None
    stop_wait_task = create_task(stop_event.wait())
    try:
        while True:
            if mon_task is None:
                stop_iteration_event = Event()
                mon_task = create_task(run_monitoring_tasks(conf, model, stop_iteration_event))
            try:
                await wait([mon_task, stop_wait_task], timeout=reload_interval_s, return_when=FIRST_COMPLETED)
            except TimeoutError:
                pass
            if not stop_event.is_set():
                # should we restart monitoring task because of changed config?
                conf.reload()
                old_conf_version = conf_version
                conf_version = conf.get_reload_version()
                if conf_version == old_conf_version:
                    # nothing changed
                    logger.debug('Configuration did not change - not reloading')
                    continue
                else:
                    logger.info('Configuration has changed - restarting monitoring tasks')

            logger.debug('Setting stop_iteration_event')
            stop_iteration_event.set()

            try:
                await wait([mon_task], timeout=shutdown_wait_s)
            except TimeoutError:
                logger.debug('Cancelling monitoring task')
                mon_task.cancel()

            try:
                await mon_task
            except CancelledError:
                pass
            except Exception as e:
                logger.exception('Monitoring task returned exception when shutting down: %r', e)

            assert mon_task.done()
            mon_task = None
            stop_iteration_event = None

            if stop_event.is_set():
                break
    finally:
        if not stop_wait_task.done():
            stop_wait_task.cancel()
        try:
            await stop_wait_task
        except CancelledError:
            pass
        except Exception as e:
            logger.exception('stop_wait_task returned exception when shutting down: %r', e)
        stop_wait_task = None

        if mon_task is not None:
            if not mon_task.done():
                logger.debug('Monitoring task is somehow still running in finally block')
                mon_task.cancel()
            try:
                await mon_task
            except CancelledError:
                pass
            except Exception as e:
                logger.exception('Monitoring task returned exception when shutting down: %r', e)
            mon_task = None


async def run_monitoring_tasks(conf, model, stop_event):
    tasks = []
    try:
        projects = await model.projects.list_all()
        for project in projects:
            checks = await project.list_checks()
            for check in checks:
                tasks.append(create_task(run_check(project=project, check=check, model=model, stop_event=stop_event)))
        stop_wait_task = create_task(stop_event.wait())
        tasks.append(stop_wait_task)
        done, pending = await wait(tasks, return_when=FIRST_COMPLETED)
        if stop_wait_task not in done:
            logger.warning('Some check task returned prematurely: %r', done)
    finally:
        for t in tasks:
            if not t.done():
                logger.debug('Cancelling task: %s', t)
                t.cancel()
        await wait(tasks)
        logger.debug('All monitoring tasks should be finished')


async def run_check(project, check, model, stop_event):
    log_prefix = f'[check:{project.id}:{check.id}]'
    try:
        while True:
            logger.debug(
                '%s Processing project id %s %r check id %s url: %r',
                log_prefix, project.id, project.name, check.id, check.url)


            await stop_event.wait()
            logger.debug('%s Stopping', log_prefix)
    except Exception as e:
        logger.debug('%s Failed: %r', log_prefix, e)
        await stop_event.wait()
