#!/bin/sh
poetry run alembic upgrade head
poetry run black .
export PYTHONPATH=$(pwd)
python3 src/runner.py