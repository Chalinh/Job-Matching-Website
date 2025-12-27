#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Load job data if not already loaded
python manage.py load_jobs || echo "Job data loading skipped or failed"

# Preload ML model to avoid timeout on first request (optional)
# python manage.py shell -c "from jobs.services.embeddings import EmbeddingService; EmbeddingService()._load_model()" || echo "Model preload skipped"
