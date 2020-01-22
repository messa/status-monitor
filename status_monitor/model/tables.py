from sqlalchemy import Table, Index, Column, Integer, String, DateTime, Boolean, MetaData, ForeignKey, ForeignKeyConstraint

metadata = MetaData()

t_sessions = Table('sessions', metadata,
    Column('id_hash', String, primary_key=True),
    Column('last_used', DateTime),
    Column('data_json', String))

t_users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('create_date', DateTime),
    Column('last_login_date', DateTime),
    Column('google_id', String, unique=True),
    Column('email', String),
    Column('name', String),
    Column('picture', String),
    Column('locale', String))

t_projects = Table('projects', metadata,
    Column('id', Integer, primary_key=True),
    Column('conf_project_id', String, unique=True))

t_checks = Table('checks', metadata,
    Column('id', Integer, primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('conf_check_id', String),
    Column('last_check_color', String), # red or green :)
    Column('last_check_date', DateTime),
    Index('idx_cpidccid', 'conf_project_id', 'conf_check_id', unique=True))

t_check_results = Table('check_results', metadata,
    Column('id', Integer, primary_key=True),
    Column('check_id', Integer, ForeignKey('checks.id'), nullable=False),
    Column('start_date', DateTime, nullable=False),
    Column('end_date', DateTime, nullable=False),
    Column('error_message', String),
    Column('status_code', Integer),
    Column('must_contain_string_present', Boolean),
    Column('cannot_contain_string_present', Boolean))

t_alerts = Table('alerts', metadata,
    Column('id', Integer, primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id'), nullable=False),
    Column('create_date', DateTime, nullable=False),
    Column('close_date', DateTime),
    Index('idx_projidcreatedt', 'project_id', 'create_date'))

t_alert_checks = Table('alert_checks', metadata,
    Column('id', Integer, primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id'),  nullable=False),
    Column('alert_id', Integer, ForeignKey("alerts.id"), nullable=False),
    Column('check_id', String, ForeignKey('checks.id'), nullable=False),
    Column('start_date', DateTime, nullable=False),
    Column('end_date', DateTime))

t_alert_notifications = Table('alert_notifications', metadata,
    Column('id', Integer, primary_key=True),
    Column('alert_id', String, ForeignKey("alerts.id"), nullable=False),
    Column('method_id', String, nullable=False), # "Slack", "PagerDuty", ...
    Column('method_data', String), # whatever data are needed for working with Slack/PagerDuty/...
    Index('idx_alertmethodid', 'alert_id', 'method_id', unique=True))
