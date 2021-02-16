#!/usr/bin/env bash

set -e
set -x


poetry run flake8 .

poetry run black --check . --diff --target-version py38
poetry run isort --check-only .