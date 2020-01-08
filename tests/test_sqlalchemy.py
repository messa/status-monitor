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
