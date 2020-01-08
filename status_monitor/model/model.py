from logging import getLogger
from sqlalchemy import create_engine

from .tables import metadata
from .users import Users
from .sessions import Sessions


logger = getLogger(__name__)


def get_model():
    engine = create_engine('sqlite:///status_monitor.sqlite')
    metadata.create_all(engine)
    return Model(engine=engine)


class Model:

    def __init__(self, engine):
        self.sessions = Sessions(engine=engine)
        self.users = Users(engine=engine)
