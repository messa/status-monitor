from collections import defaultdict, namedtuple
from logging import getLogger
from sqlalchemy.sql import select

from ..util import wrap_async
from .tables import t_current_check_statuses as t_ccs


logger = getLogger(__name__)


class Checks:

    def __init__(self, conf, engine):
        self._conf = conf
        self._engine = engine

    @wrap_async
    def list_checks_with_statuses(self, project_id):
        conf_project = self._conf.get_project_by_id(project_id)
        conf_checks = conf_project.checks
        checks = []
        with self._engine.begin() as conn:
            rows = conn.execute(select([t_ccs]).where(t_ccs.c.project_id == project_id))
            row_by_check_id = {row['check_id']: row for row in rows}
            for ch in conf_checks:
                row = row_by_check_id.get(ch.id) or defaultdict(lambda: None)
                checks.append(CheckWithStatus(
                    check=ch,
                    color=row['color'],
                    last_check_date=row['last_check_date']))
        return checks


CheckWithStatus = namedtuple('CheckWithStatus', 'check color last_check_date')
