from aiohttp import web
from aiohttp.web import RouteTableDef, json_response
from pathlib import Path
import re

from .helpers import get_session, get_user, check_user, get_model


routes = RouteTableDef()


@routes.get('/api/debug-session')
async def debug_session(request):
    session = await get_session(request)
    return json_response({'session': dict(session.items())})


@routes.get('/api/user')
async def user(request):
    user = await get_user(request)
    if user:
        return json_response({
            'user': {
                'id': user.id,
                'google_id': user.google_id,
                'email': user.email,
                'name': user.name,
                'picture': user.picture,
            },
        })
    else:
        return json_response({'user': None})


@routes.get('/api/projects')
async def projects_handler(request):
    await check_user(request)
    return json_response({
        'projects': await _export_projects(request.app['conf']),
    })


@routes.get('/api/project')
async def project_handler(request):
    await check_user(request)
    project_id = request.url.query['projectId']
    conf = request.app['conf']
    project = conf.get_project_by_id(project_id)
    return json_response({
        'project': _export_project(project),
    })


@routes.get('/api/checks')
async def checks_handler(request):
    await check_user(request)
    project_id = request.url.query['projectId']
    cwses = await get_model(request).checks.list_checks_with_statuses(project_id=project_id)
    return json_response({
        'checks': [
            {
                'check': _export_check(cws.check),
                'current_status': {
                    'color': cws.color,
                    'last_check_date': cws.last_check_date,
                },
            }
            for cws in cwses],
    })



async def _export_projects(conf):
    projects = []
    for p in conf.projects:
        projects.append(_export_project(p))
    return projects


def _export_project(p):
    return {
        'projectId': p.id,
        'name': p.name,
    }


def _export_check(conf_check):
    return {
        'id': conf_check.id,
        'url': conf_check.url,
        'must_contain': conf_check.must_contain,
        'cannot_contain': conf_check.cannot_contain,
    }

