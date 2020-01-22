from collections import defaultdict, namedtuple
from datetime import datetime
from logging import getLogger
from sqlalchemy.sql import select, and_

from ..util import wrap_async
from .tables import t_checks


logger = getLogger(__name__)


class Checks:

    def __init__(self, conf, engine):
        self._conf = conf
        self._engine = engine

    @wrap_async
    def list_checks_for_project(self, project):
        assert isinstance(project.id, int)
        assert isinstance(project.conf_project_id, str)
        checks = []
        conf_checks = self._conf.get_project_by_id(project.conf_project_id).checks
        with self._engine.begin() as conn:
            rows = conn.execute(select([t_checks]).where(t_checks.c.project_id == project.id)).fetchall()
            rows_by_ccid = {row['conf_check_id']: row for row in rows}
            for conf_check in conf_checks:
                row = rows_by_ccid.get(conf_check.id)
                if not row:
                    logger.info('Configured check %r not present in database - inserting', conf_check.id)
                    row = {
                        'project_id': project.id,
                        'conf_check_id': conf_check.id,
                    }
                    conn.execute(t_checks.insert().values(row))
                    row, = conn.execute(select([t_checks]).where(and_(
                        t_checks.c.project_id == project.id,
                        t_checks.c.conf_check_id == conf_check.id,
                    ))).fetchall()
                checks.append(Check(row, conf_check))
        return checks


class Check:

    def __init__(self, row, conf_check):
        self.id = row['id']
        self.conf_check_id = row['conf_check_id']
        self.project_id = row['project_id']
        self.last_check_date = row['last_check_date']
        self.last_check_color = row['last_check_color']
        assert self.conf_check_id == conf_check.id
        assert self.last_check_date is None or isinstance(self.last_check_date, datetime)
        self.url = conf_check.url
        self.must_contain = conf_check.must_contain
        self.cannot_contain = conf_check.cannot_contain

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id!r}>'

    def export(self):
        return {
            'id': self.id,
            'url': self.url,
            'must_contain': self.must_contain,
            'cannot_contain': self.cannot_contain,
            'last_check_date': self.last_check_date,
            'last_check_color': self.last_check_color,
        }