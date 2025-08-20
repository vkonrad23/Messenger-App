import os
import time
import sys
import psycopg2
from urllib.parse import urlparse

url = os.getenv("DATABASE_URL", "")
if not url:
    print("DATABASE_URL not set; skipping wait.")
    sys.exit(0)

parsed = urlparse(url)
scheme = (parsed.scheme or "").lower()

# Only wait when using Postgres
if not scheme.startswith("postgres"):
    print(f"Non-Postgres URL detected ('{scheme}'); skipping DB wait.")
    sys.exit(0)

parsed = urlparse(url.replace("+psycopg2", ""))
host = parsed.hostname or "db"
port = parsed.port or 5432
user = parsed.username or "app"
password = parsed.password or "app"
dbname = (parsed.path or "/messenger").lstrip("/")

for i in range(60):
    try:
        conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)
        conn.close()
        print("Database is ready")
        sys.exit(0)
    except Exception as e:
        print(f"Waiting for database... ({i+1}/60): {e}")
        time.sleep(2)

print("Database not ready after waiting; exiting")
sys.exit(1)
