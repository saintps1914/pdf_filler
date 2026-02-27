#!/usr/bin/env bash
set -euo pipefail

python3 pdffiller/manage.py migrate --noinput
exec gunicorn core.wsgi:application --chdir pdffiller --bind 0.0.0.0:${PORT}
