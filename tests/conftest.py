import logging
from logging import basicConfig, getLogger
from pathlib import Path
from pytest import fixture


basicConfig(
    format='%(asctime)s %(name)-30s %(levelname)5s: %(message)s',
    level=logging.DEBUG)

getLogger('sqlalchemy').setLevel(logging.INFO)
getLogger('sqlalchemy.engine').setLevel(logging.INFO)


@fixture
def temp_dir(tmpdir):
    return Path(str(tmpdir))
