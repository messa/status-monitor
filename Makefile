python3=python3
venv_dir=venv

check: $(venv_dir)/packages-installed
	$(venv_dir)/bin/python -m pytest -v tests

run: $(venv_dir)/packages-installed
	$(venv_dir)/bin/python -m status_monitor -v

$(venv_dir)/packages-installed: requirements.txt requirements-tests.txt
	test -d $(venv_dir) || $(python3) -m venv $(venv_dir)
	$(venv_dir)/bin/pip install -U pip wheel
	$(venv_dir)/bin/pip install -r requirements.txt
	$(venv_dir)/bin/pip install -r requirements-tests.txt
	touch $@
