from aiohttp import web
from pathlib import Path
import re


routes = web.RouteTableDef()

sample_projects = [
    { 'projectId': 'foo', 'name': 'Foo' },
    { 'projectId': 'bar', 'name': 'Bar' },
]


@routes.get('/api/projects')
async def projects_handler(request):
    return web.json_response({
        'projects': await _export_projects(request.app['conf']),
    })


@routes.get('/api/project')
async def project_handler(request):
    project_id = request.url.query['projectId']
    conf = request.app['conf']
    project = conf.get_project_by_id(project_id)
    return web.json_response({
        'project': _export_project(project),
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

