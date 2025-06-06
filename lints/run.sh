#!/bin/sh

set -ex

flake8 --color always src/ bin/*.py

ruff check --output-format concise src/ bin/*.py

pylint --output-format colorized src/ bin/*.py

pyright src/ bin/*.py

mypy src/ bin/*.py

