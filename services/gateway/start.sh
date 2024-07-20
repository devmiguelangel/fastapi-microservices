#!/bin/bash

set -e
set -o errexit
set -o pipefail
set -o nounset

while ! nc -z ${DB_HOST} ${DB_PORT}; do
  echo "Waiting for the mongo database to be ready..."
  sleep 1
done

while ! nc -z ${RABBITMQ_HOST} ${RABBITMQ_PORT}; do
  echo "Waiting for the rabbitmq server to be ready..."
  sleep 1
done

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
