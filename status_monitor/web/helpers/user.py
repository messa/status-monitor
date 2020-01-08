from aiohttp.web import HTTPFound
from logging import getLogger

from .model import get_model
from .session import get_session


logger = getLogger(__name__)


async def get_user(request):
    model = get_model(request)
    session = await get_session(request)
    if session.get('user'):
        user = await model.users.get_by_id(session['user']['user_id'])
        if user:
            if session.get('google_token'):
                # TODO: verify if the token is still valid
                pass
            return user
    return None


async def check_user(request):
    user = await get_user(request)
    if not user:
        raise HTTPFound('/login')
    logger.debug('User: %s', user)
    return user
