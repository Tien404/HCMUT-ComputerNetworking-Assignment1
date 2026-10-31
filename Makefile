PY ?= python3

check:
	$(PY) -B -m src.server --check
	$(PY) -B -m src.client.main --check

test:
	$(PY) -B -m unittest discover -s tests -v

.PHONY: check test
