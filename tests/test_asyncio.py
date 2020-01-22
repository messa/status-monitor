from asyncio import create_task, wait, sleep, FIRST_COMPLETED, CancelledError
from pytest import mark


@mark.asyncio
async def test_cancelled_task_await_throws_cancelled_error():
    t = create_task(sleep(999))
    await sleep(0.001)
    t.cancel()
    try:
        await t
    except CancelledError:
        pass # expected
    else:
        raise Exception('Expected CancelledError')


@mark.asyncio
async def test_wait_exits_immediately_when_task_already_done():
    sleep_task = create_task(sleep(0.001))
    await sleep_task
    assert sleep_task.done()
    # all following waits should return immediately and not raise TimeoutError
    await wait([sleep_task], timeout=1)
    await wait([sleep_task], timeout=1, return_when=FIRST_COMPLETED)
    sleep_task_2 = create_task(sleep(999))
    await wait([sleep_task, sleep_task_2], timeout=1, return_when=FIRST_COMPLETED)
    # cleanup
    sleep_task_2.cancel()
    try:
        await sleep_task_2
    except CancelledError:
        pass
