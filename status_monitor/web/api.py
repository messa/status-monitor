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
                'default_project_id': user.default_project_id,
            },
        })
    else:
        return json_response({'user': None})


@routes.get('/api/projects')
async def projects_handler(request):
    await check_user(request)
    projects = await get_model(request).projects.list_all()
    return json_response({
        'projects': [p.export() for p in projects],
    })


@routes.get('/api/project')
async def project_handler(request):
    await check_user(request)
    project_id = int(request.url.query['projectId'])
    project = await get_model(request).projects.get_by_id(project_id)
    return json_response({
        'project': project.export(),
    })


@routes.get('/api/checks')
async def checks_handler(request):
    await check_user(request)
    project_id = int(request.url.query['projectId'])
    project = await get_model(request).projects.get_by_id(project_id)
    checks = await project.list_checks()
    return json_response({
        'checks': [check.export() for check in checks],
    })
