#!/usr/bin/env bash

set -e

poetry run autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place core_helpers --exclude=__init__.py
poetry run black core_helpers --target-version py38
poetry run isort core_helpers