#!/usr/bin/env bash
# exit on error
set -o errexit

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Loading job data..."
python manage.py load_jobs || echo "Job data loading skipped or failed"

echo "==> Build completed successfully!"

# Preload ML model to avoid timeout on first request (optional)
# python manage.py shell -c "from jobs.services.embeddings import EmbeddingService; EmbeddingService()._load_model()" || echo "Model preload skipped"
