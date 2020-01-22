'''
Just trying how to do stuff with SQLAlchemy :)
'''

from sqlalchemy import create_engine, select
from sqlalchemy import MetaData, Table, String, Column


def test_get_value_by_col_name_from_selected_row():
    metadata = MetaData()
    t_users = Table('users', metadata,
        Column('id', String, primary_key=True),
        Column('email', String),
        Column('name', String))
    engine = create_engine('sqlite:///:memory:')
    metadata.create_all(engine)
    with engine.begin() as conn:
        conn.execute(t_users.insert(), [{'id': 'u1', 'name': 'John'}])
        conn.execute(t_users.insert().values(id='u2', name='Jane'))
        conn.execute(t_users.insert().values({'id': 'u3', 'name': 'Dave'}))
    with engine.begin() as conn:
        row = conn.execute(select([t_users]).where(t_users.c.id == 'u2')).first()
        assert row[0] == 'u2'
        assert row[t_users.c.id] == 'u2'
        assert row['id'] == 'u2'
        assert row[2] == 'Jane'
        assert row[t_users.c.name] == 'Jane'
        assert row['name'] == 'Jane'
        row = conn.execute(select([t_users.c.id, t_users.c.name]).where(t_users.c.id == 'u3')).first()
        assert row[0] == 'u3'
        assert row[t_users.c.id] == 'u3'
        assert row['id'] == 'u3'
        assert row[1] == 'Dave'
        assert row[t_users.c.name] == 'Dave'
        assert row['name'] == 'Dave'


def test_composite_primary_key():
    from sqlalchemy.exc import IntegrityError
    metadata = MetaData()
    t_ccs = Table('current_check_statuses', metadata,
        Column('project_id', String, primary_key=True),
        Column('check_id', String, primary_key=True),
        Column('color', String))
    engine = create_engine('sqlite:///:memory:')
    metadata.create_all(engine)
    with engine.begin() as conn:
        conn.execute(t_ccs.insert().values(project_id='p1', check_id='c1', color='red'))
        conn.execute(t_ccs.insert().values(project_id='p1', check_id='c2', color='green'))
        conn.execute(t_ccs.insert().values(project_id='p2', check_id='c1', color='green'))
    try:
        with engine.begin() as conn:
            conn.execute(t_ccs.insert().values(project_id='p1', check_id='c1', color='green'))
    except IntegrityError:
        pass
    else:
        raise Exception('IntegrityError was expected')


def test_select_where():
    metadata = MetaData()
    t_ccs = Table('current_check_statuses', metadata,
        Column('project_id', String, primary_key=True),
        Column('check_id', String, primary_key=True),
        Column('color', String))
    engine = create_engine('sqlite:///:memory:')
    metadata.create_all(engine)
    with engine.begin() as conn:
        conn.execute(t_ccs.insert().values(project_id='p1', check_id='c1', color='red'))
        conn.execute(t_ccs.insert().values(project_id='p1', check_id='c2', color='green'))
        conn.execute(t_ccs.insert().values(project_id='p2', check_id='c1', color='green'))
    with engine.begin() as conn:
        rows = conn.execute(select([t_ccs]).where(t_ccs.c.project_id == 'p1')).fetchall()
        assert len(rows) == 2
        rows = conn.execute(select([t_ccs]).where(t_ccs.c.project_id == 'p2')).fetchall()
        assert len(rows) == 1
        # would be cool if this worked too:
        #rows = conn.execute(select([t_ccs]).where({'project_id': 'p2'})).fetchall()
        #assert len(rows) == 1
