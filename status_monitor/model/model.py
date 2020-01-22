from logging import getLogger
from sqlalchemy import create_engine

from .checks import Checks
from .projects import Projects
from .sessions import Sessions
from .tables import metadata
from .users import Users


logger = getLogger(__name__)


def get_model(conf):
    # TODO: make db connection configurable
    engine = create_engine('sqlite:///status_monitor.sqlite')
    metadata.create_all(engine)
    return Model(conf=conf, engine=engine)


class Model:

    def __init__(self, conf, engine):
        self.checks = Checks(conf=conf, engine=engine)
        self.sessions = Sessions(engine=engine)
        self.users = Users(engine=engine)
        self.projects = Projects(engine=engine, conf=conf, model=self)
