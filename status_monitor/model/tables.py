from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey

metadata = MetaData()
t_sessions = Table('sessions', metadata,
    Column('id_hash', String, primary_key=True),
    Column('last_used', DateTime),
    Column('data_json', String))

t_users = Table('users', metadata,
    Column('id', String, primary_key=True),
    Column('create_date', DateTime),
    Column('last_login_date', DateTime),
    Column('google_id', String, unique=True),
    Column('email', String),
    Column('name', String),
    Column('picture', String),
    Column('locale', String))
