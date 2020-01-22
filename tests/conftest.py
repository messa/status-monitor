from asyncio import get_event_loop
import logging
from logging import basicConfig, getLogger
from pathlib import Path
from pytest import fixture


#basicConfig(
#    format='%(asctime)s %(name)-30s %(levelname)5s: %(message)s',
#    level=logging.DEBUG)

#getLogger('sqlalchemy').setLevel(logging.INFO)
#getLogger('sqlalchemy.engine').setLevel(logging.INFO)


@fixture
def temp_dir(tmpdir):
    return Path(str(tmpdir))


@fixture
def loop():
    return get_event_loop()


@fixture
def engine(temp_dir):
    from sqlalchemy import create_engine
    from uuid import uuid4
    from status_monitor.model.tables import metadata
    db_path = temp_dir / f'{uuid4()}.sqlite'
    engine = create_engine(f'sqlite:///{db_path}')
    try:
        metadata.create_all(engine)
        yield engine
    finally:
        engine.dispose()
