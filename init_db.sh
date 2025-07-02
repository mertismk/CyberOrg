#!/bin/bash
set -e

# Wait for PostgreSQL to be ready
until pg_isready -h localhost -U cyberorg -d cyberorg; do
  echo "Waiting for postgres..."
  sleep 1
done

echo "PostgreSQL is up - executing command"

# Import the database dump
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" < /docker-entrypoint-initdb.d/cyberorg_db_dump.sql 