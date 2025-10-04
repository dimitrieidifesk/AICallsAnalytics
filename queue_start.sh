#!/bin/sh
echo 'run scheduler'
export PYTHONPATH=$(pwd)
python3 src/queue_app.py