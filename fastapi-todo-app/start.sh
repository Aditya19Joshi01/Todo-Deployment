#!/bin/sh
set -e

echo "Waiting for Postgres to be available..."
python - <<'PY'
import os, time, sys
try:
    import psycopg2
except Exception:
    # if psycopg2 isn't available, skip waiting (likely sqlite fallback)
    sys.exit(0)

url = os.environ.get('DATABASE_URL')
if not url or url.startswith('sqlite'):
    # nothing to wait for when using sqlite
    sys.exit(0)

from urllib.parse import urlparse
p = urlparse(url)
host = p.hostname or 'db'
port = p.port or 5432
user = p.username
password = p.password
dbname = p.path.lstrip('/') if p.path else ''

while True:
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)
        conn.close()
        print('Postgres is available')
        break
    except Exception as exc:
        print('Postgres not ready, retrying in 1s...')
        time.sleep(1)
PY

echo "Running Alembic migrations (if any)..."
python -m alembic -c alembic.ini upgrade head || true

echo "Starting Uvicorn..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info
