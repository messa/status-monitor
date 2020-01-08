from aiohttp import web
from aiohttp.web import RouteTableDef, Response, HTTPFound
from functools import wraps
from logging import getLogger
from requests_oauthlib import OAuth2Session

from ..util import wrap_async
from .helpers import with_session, get_model


# based on https://requests-oauthlib.readthedocs.io/en/latest/examples/google.html

# OAuth endpoints given in the Google API documentation
authorization_base_url = 'https://accounts.google.com/o/oauth2/v2/auth'
token_url = 'https://www.googleapis.com/oauth2/v4/token'

routes = RouteTableDef()

logger = getLogger(__name__)


@routes.get('/api/auth/google')
@with_session
async def index_handler(request, session):

    logger.debug('-----------------------------------------------------------------------------')
    logger.debug('URL: %s', request.url)
    logger.debug('Headers: %s', request.headers)

    google_conf = request.app['conf'].google_oauth
    scope = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
    ]
    google = OAuth2Session(google_conf.client_id, scope=scope, redirect_uri=google_conf.redirect_uri)
    authorization_url, state = google.authorization_url(authorization_base_url,
        access_type='offline', prompt='select_account')
    session['google_oauth_state'] = state
    raise HTTPFound(location=authorization_url)


@routes.get('/api/auth/google-callback')
@with_session
async def index_handler(request, session):

    logger.debug('-----------------------------------------------------------------------------')
    logger.debug('URL: %s', request.url)
    logger.debug('Headers: %s', request.headers)

    google_conf = request.app['conf'].google_oauth
    if request.url.query['state'] != session.pop('google_oauth_state', None):
        logger.info('State mismatch')
        raise HTTPFound('/login?error=state-mismatch')

    @wrap_async
    def fetch_token():
        google = OAuth2Session(google_conf.client_id, redirect_uri=google_conf.redirect_uri)
        token = google.fetch_token(token_url,
            client_secret=google_conf.client_secret,
            code=request.url.query['code'],
            timeout=120)
        logger.debug('Token: %r', token)
        assert isinstance(token, dict)
        r = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
        profile = r.json()
        logger.debug('Profile: %r', profile)
        return token, profile

    try:
        token, profile = await fetch_token()
    except Exception as e:
        if 'InvalidGrantError' in repr(e):
            raise HTTPFound('/login?error=invalid-grant')
        else:
            raise HTTPFound('/login?error=google-auth-failed')

    if not profile['verified_email']:
        raise HTTPFound('/login?error=email-not-verified')

    # TODO: limit who can login according to configuration

    # TODO: should we do something with profile.get('hd')?

    user = await get_model(request).users.get_user_after_oauth(
        google_id=profile['id'],
        email=profile['email'],
        name=profile['name'],
        picture=profile['picture'],
        locale=profile['locale'])

    session['user'] = {
        'google_id': profile['id'],
        'user_id': user.id,
        'google_token': token,
        'google_profile': profile,
    }

    raise HTTPFound('/dashboard')
    #return Response(status=302, headers={'Location': '/dashboard'})
