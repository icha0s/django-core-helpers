#!/usr/bin/env bash

set -e

poetry run autoflake --recursive --remove-all-unused-imports --remove-unused-variables --in-place . --exclude=__init__.py
poetry run black . --target-version py38
poetry run isort .