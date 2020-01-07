from asyncio import get_running_loop
from base64 import urlsafe_b64encode
from datetime import datetime
import hashlib
from logging import getLogger
from simplejson import dumps as json_dumps
from simplejson import loads as json_loads
from sqlalchemy.sql import select

from ..util import wrap_async
from .tables import t_sessions


logger = getLogger(__name__)


class Sessions:

    def __init__(self, engine):
        self._engine = engine

    @wrap_async
    def load_session(self, session_id):
        assert isinstance(session_id, str)
        hashed_id = get_hashed_session_id(session_id)
        with self._engine.begin() as conn:
            r = conn.execute(select([t_sessions]).where(t_sessions.c.id_hash == hashed_id))
            row = r.first()
            if row:
                assert row[t_sessions.c.id_hash] == hashed_id
                return json_loads(row[t_sessions.c.data_json])
            else:
                return None

    @wrap_async
    def update_session(self, session_id, changes):
        assert isinstance(session_id, str)
        assert isinstance(changes, dict)
        hashed_id = get_hashed_session_id(session_id)
        with self._engine.begin() as conn:
            r = conn.execute(select([t_sessions]).where(t_sessions.c.id_hash == hashed_id))
            row = r.first()
            if row:
                assert row[t_sessions.c.id_hash] == hashed_id
                orig_data = json_loads(row[t_sessions.c.data_json])
                new_data = {**orig_data, **changes}
                assert {new_data[k] == changes[k] for k in changes}
                conn.execute(
                    t_sessions.update()
                        .where(t_sessions.c.id_hash == hashed_id)
                        .values(
                            last_used=datetime.utcnow(),
                            data_json=json_dumps(new_data)))
            else:
                conn.execute(
                    t_sessions.insert().values(
                        id_hash=hashed_id,
                        last_used=datetime.utcnow(),
                        data_json=json_dumps(changes)))


def get_hashed_session_id(raw_session_id):
    hash_bytes = hashlib.sha1(raw_session_id.encode('ascii')).digest()
    hash_b64 = urlsafe_b64encode(hash_bytes).decode('ascii')
    return hash_b64.rstrip('=')


assert get_hashed_session_id('foo') == 'C-7Hteo_D9vJXQ3UfzxbwnXaijM'
