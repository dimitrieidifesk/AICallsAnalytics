#!/bin/sh
poetry run alembic upgrade head
poetry run black .
export PYTHONPATH=$(pwd)
# poetry run python -m src.runner
python3 src/runner.py