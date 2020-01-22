from base64 import urlsafe_b64encode
from functools import partial
import hashlib
import os
from pathlib import Path
import re
import yaml


def get_configuration(cfg_path):
    cfg_path = Path(cfg_path)
    return ReloadWrapper(Configuration, cfg_path)


class ReloadWrapper:

    def __init__(self, factory, file_path):
        self._factory = factory
        self._file_path = file_path
        self._value = None
        self._stat_snapshot = None
        self.reload()

    def _get_stat_snapshot(self, open_file):
        st = os.fstat(open_file.fileno())
        return (st.st_size, st.st_mtime)

    def reload(self):
        with self._file_path.open('rb') as f:
            sn = self._get_stat_snapshot(f)
            if sn != self._stat_snapshot:
                self._value = self._factory(self._file_path, f.read())
                self._stat_snapshot = sn

    def get_reload_version(self):
        return self._stat_snapshot

    def __getattr__(self, name):
        return getattr(self._value, name)


def check_list(value):
    if not isinstance(value, list):
        raise Exception(f'list was expected instead of {value!r}')
    return value


class Configuration:

    def __init__(self, cfg_path, cfg_bytes):
        assert isinstance(cfg_bytes, bytes)
        cfg = yaml.safe_load(cfg_bytes.decode())
        self.log_file = cfg_path / cfg['log_file'] if cfg.get('log_file') else None
        self.google_oauth = GoogleOAuth(cfg['google_oauth'])
        self.projects = [Project(p) for p in cfg['projects']]
        verify_that_project_ids_are_unique(self.projects)
        self.session_cookie_name = cfg.get('session_cookie_name', 'STATUS_MONITOR_SESSION')

    def get_project_by_id(self, project_id):
        for p in self.projects:
            if p.id == project_id:
                return p
        raise ProjectNotFoundError(f'Project id {project_id!r} not found')


def verify_that_project_ids_are_unique(projects):
    by_id = {}
    for p in projects:
        if not p.id:
            raise Exception(f'Project has no id: {p}')
        assert isinstance(p.id, str)
        if p.id in by_id:
            raise Exception(f'There are two projects with the same id: {p} abd {by_id[p.id]}')
        by_id[p.id] = p


class ProjectNotFoundError (Exception):
    pass


class GoogleOAuth:

    def __init__(self, cfg):
        self.client_id = cfg['client_id']
        self.client_secret = cfg['client_secret']
        self.redirect_uri = cfg['redirect_uri']


class Project:

    def __init__(self, cfg):
        self.id = cfg['id']
        try:
            self.name = cfg['name']
            self.allow_email = check_list(cfg.get('allow_email') or [])
            self.allow_email_regex_raw = check_list(cfg.get('allow_email_regex') or [])
            self.allow_email_regex = [re.compile(x) for x in self.allow_email_regex_raw]
            self.checks = []
            for ch in cfg['checks']:
                if not ch.get('type') or ch['type'] == 'http':
                    self.checks.append(HTTPCheck(ch))
                else:
                    raise Exception(f"Unknown check type: {ch['type']!r}")
            verify_that_check_ids_are_unique(self.checks)
        except Exception as e:
            raise Exception(f'Failed to process configuration of project {self.id}: {e}')


def verify_that_check_ids_are_unique(checks):
    by_id = {}
    for ch in checks:
        if not ch.id:
            raise Exception(f'Check has no id: {ch}')
        assert isinstance(ch.id, str)
        if ch.id in by_id:
            raise Exception(f'There are two checks with the same id: {ch} abd {by_id[ch.id]}')
        by_id[ch.id] = ch


class HTTPCheck:

    def __init__(self, cfg):
        self.id = cfg.get('id') or generate_check_id(url=cfg['url'])
        self.url = cfg['url']
        self.must_contain = cfg.get('must_contain')
        self.cannot_contain = cfg.get('cannot_contain')


def generate_check_id(url):
    h_bytes = hashlib.sha3_256(url.encode()).digest()
    h_b64 = urlsafe_b64encode(h_bytes).decode()
    return 'C' + h_b64.replace('_', '').replace('-', '')[:7]


assert generate_check_id('http://example.com') == 'CXjaiiW2'
