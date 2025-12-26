from django.core.management.base import BaseCommand
from jobs.models import Job
import json
from pathlib import Path
from datetime import datetime


class Command(BaseCommand):
    help = 'Load normalized job data from JSON into database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default='data/normalized_data/camhr_normalized_v3_20251226_180932.json',
            help='Path to normalized job JSON file'
        )

    def handle(self, *args, **options):
        file_path = Path(options['file'])

        if not file_path.exists():
            # Try relative to project root
            file_path = Path(__file__).resolve().parent.parent.parent.parent / options['file']

        if not file_path.exists():
            self.stdout.write(self.style.ERROR(f'File not found: {options["file"]}'))
            return

        self.stdout.write(f'Loading jobs from: {file_path}')

        # Load JSON data
        with open(file_path, 'r', encoding='utf-8') as f:
            jobs_data = json.load(f)

        self.stdout.write(f'Found {len(jobs_data)} jobs in file')

        # Clear existing jobs
        Job.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing jobs from database'))

        # Prepare job objects for bulk insert
        job_objects = []

        for job_data in jobs_data:
            # Parse dates
            pubdate = None
            expdate = None

            if job_data.get('pubdate'):
                try:
                    pubdate = datetime.fromisoformat(job_data['pubdate'])
                except (ValueError, TypeError):
                    pass

            if job_data.get('expdate'):
                try:
                    expdate = datetime.fromisoformat(job_data['expdate'])
                except (ValueError, TypeError):
                    pass

            job_obj = Job(
                job_id=job_data['job_id'],
                job_title=job_data.get('job_title', ''),
                company=job_data.get('company', ''),
                location=job_data.get('location', ''),
                industry=job_data.get('industry', ''),
                min_years_experience=job_data.get('experience', {}).get('min_years', 0),
                education_level=job_data.get('education', {}).get('level', ''),
                education_major=job_data.get('education', {}).get('major', ''),
                skills=job_data.get('skills', []),
                languages=job_data.get('languages', []),
                raw_text=job_data.get('raw_text', ''),
                pubdate=pubdate,
                expdate=expdate
            )
            job_objects.append(job_obj)

        # Bulk create for performance
        Job.objects.bulk_create(job_objects, batch_size=100)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully loaded {len(job_objects)} jobs into database!'
        ))

        # Print statistics
        total_skills = sum(len(job.skills) for job in job_objects)
        avg_skills = total_skills / len(job_objects) if job_objects else 0

        jobs_with_education = sum(1 for job in job_objects if job.education_level)
        jobs_with_major = sum(1 for job in job_objects if job.education_major)

        self.stdout.write('\n' + '='*60)
        self.stdout.write('DATABASE LOAD STATISTICS')
        self.stdout.write('='*60)
        self.stdout.write(f'Total Jobs:              {len(job_objects)}')
        self.stdout.write(f'Total Skills:            {total_skills}')
        self.stdout.write(f'Avg Skills per Job:      {avg_skills:.1f}')
        self.stdout.write(f'Jobs with Education:     {jobs_with_education} ({100*jobs_with_education/len(job_objects):.1f}%)')
        self.stdout.write(f'Jobs with Major:         {jobs_with_major} ({100*jobs_with_major/len(job_objects):.1f}%)')
        self.stdout.write('='*60)
