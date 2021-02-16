#!/usr/bin/env bash

set -e
set -x


poetry run flake8 core_helpers
poetry run mypy --show-error-codes core_helpers

poetry run black --check . --diff --target-version py38
poetry run isort --check-only core_helpers