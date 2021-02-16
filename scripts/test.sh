#!/usr/bin/env bash

set -e
set -x

poetry run pytest --cov=core_helpers --cov=tests --cov-report=term-missing --cov-report=xml --cov-config=setup.cfg ${@}
