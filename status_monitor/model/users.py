from datetime import datetime
from logging import getLogger
from secrets import token_urlsafe
from sqlalchemy.sql import select

from ..util import wrap_async
from .tables import t_users


logger = getLogger(__name__)


class Users:

    def __init__(self, engine):
        self._engine = engine

    @wrap_async
    def get_by_id(self, user_id):
        with self._engine.begin() as conn:
            r = conn.execute(select([t_users]).where(t_users.c.id == user_id))
            row = r.first()
            if row:
                return User(row=row)
            else:
                return None

    @wrap_async
    def get_user_after_oauth(self, email, name, picture, locale, google_id):
        with self._engine.begin() as conn:
            if google_id:
                row = conn.execute(select([t_users]).where(t_users.c.google_id == google_id)).first()
                if not row:
                    row = {
                        'email': email,
                        'google_id': google_id,
                        'name': name,
                        'picture': picture,
                        'locale': locale,
                        'create_date': datetime.utcnow(),
                    }
                    conn.execute(t_users.insert().values(row))
                    row, = conn.execute(select([t_users]).where(t_users.c.google_id == google_id)).fetchall()
                user = User(row=row)
            else:
                raise Exception('google_id must be provided')
            user._sync_update_last_login_date(conn)
            user._sync_update_after_oauth(conn,
                email=email,
                name=name,
                picture=picture,
                locale=locale)
            return user


class User:

    def __init__(self, row):
        self.id = row['id']
        self.google_id = row['google_id']
        self.email = row['email']
        self.name = row['name']
        self.picture = row['picture']
        self.locale = row['locale']

    def __repr__(self):
        cls = self.__class__.__name__
        return f'<{cls} id={self.id!r} google_id={self.google_id!r} email={self.email!r}>'

    def _sync_update_last_login_date(self, conn):
            conn.execute(
                t_users.update()
                    .where(t_users.c.id == self.id)
                    .values(last_login_date=datetime.utcnow()))

    def _sync_update_after_oauth(self, conn, email, name, picture, locale):
        update = {}
        if email != self.email:
            update['email'] = email
        if name != self.name:
            update['name'] = name
        if picture != self.picture:
            update['picture'] = picture
        if locale and not self.locale:
            update['locale'] = locale
        if update:
            conn.execute(
                t_users.update()
                    .where(t_users.c.id == self.id)
                    .values(update))
            self.__dict__.update(update)




'''
        user = model.users.get_by_id(session['user']['user_id'])
    user = get_model(request).users.get_user_after_oauth(
        google_id=profile['id'],
        email=profile['email'],
        name=profile['name'],
        picture=profile['picture'],
        locale=profile['locale'])
'''
