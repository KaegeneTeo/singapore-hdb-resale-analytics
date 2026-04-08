#!/bin/bash
set -e

echo "Starting PostgreSQL via Docker Compose..."
docker-compose up -d

# Wait for PostgreSQL to fully accept connections for the specific user/db
echo "Waiting for PostgreSQL to be ready..."
until docker exec hdb_postgres pg_isready -U hdbuser -d hdbresale > /dev/null 2>&1; do
  echo "  still waiting..."
  sleep 2
done
echo "PostgreSQL is ready."

echo "Loading CSV to database (if needed)..."
python src/load_to_db.py

echo "Transforming data..."
python src/transform.py

echo "Launching Dash app..."
python app/main.py