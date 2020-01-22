from pytest import fixture, mark
from textwrap import dedent

from status_monitor.configuration import get_configuration
from status_monitor.model.projects import Projects


@fixture
def conf(temp_dir):
    cfg_path = temp_dir / 'conf.yaml'
    cfg_path.write_text(dedent('''
        google_oauth:
          client_id: null
          client_secret: null
          redirect_uri: null
        projects:
        - id: demo
          name: Demo
          allow_email: []
          allow_email_regex:
          - ".*@gmail.com"
          checks:
          - url: https://ip.messa.cz/
          - url: https://image-url-preview.now.sh/
            must_contain: "Example:"
    '''))
    return get_configuration(cfg_path)


def test_conf(conf):
    assert conf
    assert len(conf.projects) == 1
    assert conf.projects[0].id == 'demo'
    assert conf.projects[0].name == 'Demo'


@mark.asyncio
async def test_list_projects(loop, engine, conf):
    projects_model = Projects(engine=engine, conf=conf, model=None)
    for i in range(2):
        projects = await projects_model.list_all()
        assert len(projects) == 1
        assert projects[0].id == 1
        assert projects[0].conf_project_id == 'demo'
        assert projects[0].name == 'Demo'
