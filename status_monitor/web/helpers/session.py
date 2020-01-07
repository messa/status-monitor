from aiohttp.web import HTTPException, StreamResponse, Response
from copy import deepcopy
from functools import wraps
from inspect import iscoroutinefunction
from logging import getLogger
from secrets import token_urlsafe


logger = getLogger(__name__)


def get_cookie_name(request):
    return request.app['conf'].session_cookie_name or 'SESSION'


class Session:

    def __init__(self, request, session_id, data):
        assert isinstance(session_id, str)
        assert isinstance(data, dict) or data is None
        self._session_id = session_id
        self._request = request
        self._original_data = data or {}
        self._data = deepcopy(self._original_data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        return value

    def pop(self, *args, **kwargs):
        return self._data.pop(*args, **kwargs)

    def get_changes(self):
        assert isinstance(self._data, dict)
        assert isinstance(self._original_data, dict)
        changes = {}
        all_keys = self._original_data.keys() | self._data.keys()
        for k in all_keys:
            if self._data.get(k) != self._original_data.get(k):
                changes[k] = self._data.get(k)
        return changes

    async def save(self):
        changes = self.get_changes()
        if changes:
            logger.debug('Session changes: %r', changes)
            model = self._request.app['model']
            await model.sessions.update_session(self._session_id, changes)
            self._original_data = deepcopy(self._data)


async def get_session(request):
    if not request.get('session'):
        cookie_name = get_cookie_name(request)
        cookie_value = request.cookies.get(cookie_name)
        if cookie_value:
            session_data = await request.app['model'].sessions.load_session(session_id=cookie_value)
        else:
            cookie_value = token_urlsafe(24)
            request['set_session_cookie_value'] = cookie_value
            session_data = None
        request['session'] = Session(request=request, session_id=cookie_value, data=session_data)
    return request['session']


def insert_session_into_response(request, response):
    assert isinstance(response, Response)
    v = request.pop('set_session_cookie_value', None)
    if v:
        cookie_name = get_cookie_name(request)
        # https://docs.aiohttp.org/en/stable/web_reference.html#aiohttp.web.StreamResponse.set_cookie
        # TODO: figure out when to send secure=True
        response.set_cookie(cookie_name, v, max_age=86400 * 30, httponly=True)


def with_session(handler):
    assert iscoroutinefunction(handler)

    @wraps(handler)
    async def wrapper(request, **kwargs):
        session = await get_session(request)

        raise_response = False
        try:
            response = await handler(request, session=session, **kwargs)
        except HTTPException as e:
            response = e
            raise_response = True

        await session.save()

        assert isinstance(response, StreamResponse)
        if isinstance(response, Response):
            # otherwise likely got websocket or streaming
            insert_session_into_response(request, response)

        if raise_response:
            raise response
        else:
            return response

    return wrapper
