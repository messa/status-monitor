from pytest import fixture, mark
from textwrap import dedent

from status_monitor.configuration import get_configuration
from status_monitor.model.projects import Projects
from status_monitor.model.checks import Checks


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


@fixture
def model(engine, conf):
    class Model:
        def __init__(self):
            self.projects = Projects(engine=engine, conf=conf, model=self)
            self.checks = Checks(engine=engine, conf=conf)
    return Model()


def test_model(model):
    assert model


@mark.asyncio
async def test_list_checks(loop, model):
    project, = await model.projects.list_all()
    for i in range(2):
        checks = await project.list_checks()
        assert len(checks) == 2
        assert checks[0].url == 'https://ip.messa.cz/'
        assert checks[1].url == 'https://image-url-preview.now.sh/'
        assert checks[0].export() == {
            'id': 1,
            'url': 'https://ip.messa.cz/',
            'last_check_color': None,
            'last_check_date': None,
            'must_contain': None,
            'cannot_contain': None,
        }

