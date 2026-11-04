PY ?= python3

test:
	$(PY) -B -m unittest discover -s tests -v

.PHONY: test
