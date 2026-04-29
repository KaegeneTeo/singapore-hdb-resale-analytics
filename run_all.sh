#!/bin/bash
set -e

echo "Starting MySQL via Docker Compose..."
docker-compose up -d

# Wait for MySQL to be ready
echo "Waiting for MySQL to be ready..."
until docker exec hdb_mysql mysqladmin ping -h"127.0.0.1" --silent; do
  echo "  still waiting..."
  sleep 2
done
echo "MySQL is ready."

echo "Loading CSV to database (if needed)..."
python src/load_to_db.py

echo "Transforming data..."
python src/transform.py

echo "Launching Dash app..."
python -m app.main