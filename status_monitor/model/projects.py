from logging import getLogger
from sqlalchemy import select

from ..util import wrap_async
from .tables import t_projects


logger = getLogger(__name__)


class Projects:

    def __init__(self, engine, conf, model):
        self._engine = engine
        self._conf = conf
        self._model = model

    @wrap_async
    def list_all(self):
        projects = []
        conf_projects = {p.id: p for p in self._conf.projects}
        processed_conf_project_ids = set()
        with self._engine.begin() as conn:
            rows = conn.execute(select([t_projects])).fetchall()
            rows_by_cpid = {row['conf_project_id']: row for row in rows}
            for conf_project in self._conf.projects:
                assert conf_project.id
                row = rows_by_cpid.get(conf_project.id)
                if not row:
                    logger.info('Configured project %r not present in database - insering', conf_project.id)
                    row = {'conf_project_id': conf_project.id}
                    conn.execute(t_projects.insert().values(row))
                    row, = conn.execute(select([t_projects]).where(t_projects.c.conf_project_id == conf_project.id)).fetchall()
                projects.append(Project(row, conf_project, model=self._model))
        return projects

    @wrap_async
    def get_by_id(self, project_id):
        assert isinstance(project_id, int)
        with self._engine.begin() as conn:
            row = conn.execute(select([t_projects]).where(t_projects.c.id == project_id)).first()
            conf_project = self._conf.get_project_by_id(row['conf_project_id'])
            return Project(row, conf_project, model=self._model)


class Project:

    def __init__(self, row, conf_project, model):
        '''
        row: database row from table projects
        conf_project: data from configuration
        '''
        self.id = row['id']
        self.conf_project_id = row['conf_project_id']
        assert self.conf_project_id == conf_project.id
        self.name = conf_project.name
        self.allow_email = conf_project.allow_email
        #self.allow_email_regex_raw = conf_project.allow_email_regex_raw
        self.allow_email_regex = conf_project.allow_email_regex
        self._model = model

    def __repr__(self):
        return f'<{self.__class__.__name__} id={self.id!r}>'

    async def list_checks(self):
        return await self._model.checks.list_checks_for_project(project=self)

    def export(self):
        return {
            'id': self.id,
            'name': self.name,
        }
