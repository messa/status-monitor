from pathlib import Path


def test_import():
    import status_monitor


def test_sha3_256():
    import hashlib
    h = hashlib.sha3_256(b'Lorem ipsum').hexdigest()
    assert h == '722755290da497f8d4367eb377b354cd4ac41d29744116a1550fdadd3c4e1cdc'


def test_load_sample_configuration():
    from status_monitor.configuration import get_configuration
    here = Path(__file__).absolute().parent
    project_dir = here.parent
    sample_conf_path = project_dir / 'sample_configuration.yaml'
    assert sample_conf_path.is_file()
    conf = get_configuration(sample_conf_path)
    assert conf
