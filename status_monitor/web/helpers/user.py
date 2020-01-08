from aiohttp.web import HTTPForbidden
from logging import getLogger
from simplejson import dumps as json_dumps

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
        logger.debug('Not logged in, raising HTTPForbidden')
        raise HTTPForbidden(content_type='text/plain', text=json_dumps({'error_code': 'not_logged_in'}))
    logger.debug('User: %s', user)
    return user
