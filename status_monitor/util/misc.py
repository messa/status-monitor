from asyncio import get_running_loop
from functools import partial, wraps


def wrap_async(f):
    @wraps(f)
    async def wrapped(*args, **kwargs):
        loop = get_running_loop()
        return await loop.run_in_executor(None, partial(f, *args, **kwargs))

    return wrapped
