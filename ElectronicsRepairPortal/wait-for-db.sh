#!/bin/sh

set -e

host="$DB_HOST"
port="${DB_PORT:-3306}"

echo "⏳ Waiting for MySQL to be ready at $host:$port..."

until nc -z "$host" "$port"; do
  sleep 1
done

echo "✅ MySQL is up — launching"

exec "$@"
