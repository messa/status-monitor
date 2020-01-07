from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey

metadata = MetaData()

t_sessions = Table('sessions', metadata,
    Column('id_hash', String, primary_key=True),
    Column('last_used', DateTime),
    Column('data_json', String))
