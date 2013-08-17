#!/bin/bash

set -e

cd /path/to/project/root
source venv/bin/activate
exec gunicorn app:app -c "server/gunicorn.conf.py"
