"""
Management command to load job data from JSON file into the database.

Usage:
    python manage.py load_jobs [--file path/to/file.json] [--clear]

Options:
    --file: Path to JSON file (default: latest normalized data)
    --clear: Clear existing jobs before loading
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from jobs.models import Job
import json
from pathlib import Path
from django.conf import settings


class Command(BaseCommand):
    help = 'Load job data from JSON file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Path to JSON file containing job data',
            default=None
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing jobs before loading'
        )

    def handle(self, *args, **options):
        # Determine file path
        if options['file']:
            file_path = Path(options['file'])
        else:
            # Use latest normalized data
            normalized_dir = Path(settings.BASE_DIR) / 'data' / 'normalized_data'
            if not normalized_dir.exists():
                self.stdout.write(self.style.ERROR(
                    f'Directory not found: {normalized_dir}'
                ))
                return

            # Find latest normalized file
            json_files = sorted(normalized_dir.glob('camhr_normalized_*.json'))
            if not json_files:
                self.stdout.write(self.style.ERROR(
                    f'No normalized job data files found in {normalized_dir}'
                ))
                return

            file_path = json_files[-1]  # Get latest file

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(
                f'File not found: {file_path}'
            ))
            return

        self.stdout.write(f'Loading jobs from: {file_path}')

        # Load JSON data
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                jobs_data = json.load(f)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(
                f'Invalid JSON file: {e}'
            ))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error reading file: {e}'
            ))
            return

        # Clear existing jobs if requested
        if options['clear']:
            deleted_count = Job.objects.count()
            Job.objects.all().delete()
            self.stdout.write(self.style.WARNING(
                f'Cleared {deleted_count} existing jobs'
            ))

        # Load jobs into database
        loaded = 0
        skipped = 0
        errors = 0

        with transaction.atomic():
            for job_data in jobs_data:
                try:
                    # Extract job ID
                    job_id = job_data.get('job_id')
                    if not job_id:
                        self.stdout.write(self.style.WARNING(
                            f'Skipping job without job_id'
                        ))
                        skipped += 1
                        continue

                    # Check if job already exists
                    if Job.objects.filter(job_id=job_id).exists():
                        skipped += 1
                        continue

                    # Create job object
                    Job.objects.create(
                        job_id=job_data.get('job_id'),
                        job_title=job_data.get('job_title', ''),
                        company=job_data.get('company', ''),
                        location=job_data.get('location', ''),
                        industry=job_data.get('industry', ''),
                        min_years_experience=job_data.get('min_years_experience', 0),
                        education_level=job_data.get('education_level', ''),
                        education_major=job_data.get('education_major', ''),
                        skills=job_data.get('skills', []),
                        languages=job_data.get('languages', []),
                        raw_text=job_data.get('raw_text', ''),
                        pubdate=job_data.get('pubdate'),
                        expdate=job_data.get('expdate')
                    )
                    loaded += 1

                    if loaded % 100 == 0:
                        self.stdout.write(f'Loaded {loaded} jobs...')

                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Error loading job {job_data.get("job_id", "unknown")}: {e}'
                    ))
                    errors += 1

        # Summary
        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Successfully loaded {loaded} jobs'
        ))
        if skipped > 0:
            self.stdout.write(self.style.WARNING(
                f'⚠ Skipped {skipped} jobs (already exist or invalid)'
            ))
        if errors > 0:
            self.stdout.write(self.style.ERROR(
                f'✗ {errors} errors occurred'
            ))

        # Show total count
        total = Job.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f'\nTotal jobs in database: {total}'
        ))
