from django.core.management.base import BaseCommand
from django.db import connection
from django.conf import settings


class Command(BaseCommand):
    help = 'Setup PostgreSQL database and user automatically'

    def handle(self, *args, **options):
        """
        Create PostgreSQL database and user automatically
        Connects to default 'postgres' database to create the new database
        """
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']

        self.stdout.write(self.style.WARNING(
            '\n' + '='*60 + '\n'
            'AUTOMATIC DATABASE SETUP\n'
            + '='*60
        ))

        self.stdout.write(f'\nTarget Database: {db_name}')
        self.stdout.write(f'Target User: {db_user}')
        self.stdout.write(f'Target Password: {db_password}\n')

        # Instructions for manual setup (PostgreSQL requires superuser to create database)
        self.stdout.write(self.style.WARNING(
            '\nNOTE: PostgreSQL requires superuser access to create databases.'
        ))
        self.stdout.write(self.style.WARNING(
            'You have two options:\n'
        ))

        self.stdout.write(self.style.SUCCESS(
            '\n--- OPTION 1: Automatic (Recommended) ---'
        ))
        self.stdout.write('Run this in PowerShell/Command Prompt with postgres password:\n')

        commands = f'''psql -U postgres -c "CREATE DATABASE {db_name};"
psql -U postgres -c "CREATE USER {db_user} WITH PASSWORD '{db_password}';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"
psql -U postgres -d {db_name} -c "GRANT ALL ON SCHEMA public TO {db_user};"
psql -U postgres -c "ALTER ROLE {db_user} SET client_encoding TO 'utf8';"
psql -U postgres -c "ALTER ROLE {db_user} SET default_transaction_isolation TO 'read committed';"
psql -U postgres -c "ALTER ROLE {db_user} SET timezone TO 'UTC';"'''

        self.stdout.write(self.style.SUCCESS(commands))

        self.stdout.write(self.style.SUCCESS(
            '\n--- OPTION 2: Use Batch Script (Easiest) ---'
        ))
        self.stdout.write('I can create a batch script for you. Run:\n')
        self.stdout.write(self.style.SUCCESS(
            'python manage.py create_db_script'
        ))
        self.stdout.write('\nThen run: setup_database.bat\n')

        self.stdout.write(self.style.WARNING(
            '\n--- OPTION 3: Manual (pgAdmin) ---'
        ))
        self.stdout.write('1. Open pgAdmin 4')
        self.stdout.write('2. Right-click Databases → Create → Database')
        self.stdout.write(f'3. Name: {db_name}')
        self.stdout.write('4. Open Query Tool and run:\n')

        manual_sql = f'''CREATE USER {db_user} WITH PASSWORD '{db_password}';
GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};
GRANT ALL ON SCHEMA public TO {db_user};
ALTER ROLE {db_user} SET client_encoding TO 'utf8';
ALTER ROLE {db_user} SET default_transaction_isolation TO 'read committed';
ALTER ROLE {db_user} SET timezone TO 'UTC';'''

        self.stdout.write(self.style.SUCCESS(manual_sql))

        # Try to verify database exists
        self.stdout.write('\n' + '='*60)
        self.stdout.write('VERIFICATION')
        self.stdout.write('='*60 + '\n')

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT version();")
                version = cursor.fetchone()[0]
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Connected to PostgreSQL: {version[:50]}...'
                ))

                cursor.execute("SELECT current_database();")
                current_db = cursor.fetchone()[0]
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Current database: {current_db}'
                ))

                self.stdout.write(self.style.SUCCESS(
                    '\n✓ Database is ready! You can now run:'
                ))
                self.stdout.write(self.style.SUCCESS(
                    '  python manage.py migrate'
                ))
                self.stdout.write(self.style.SUCCESS(
                    '  python manage.py load_jobs'
                ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'\n✗ Cannot connect to database: {e}'
            ))
            self.stdout.write(self.style.WARNING(
                '\nPlease create the database using one of the options above.'
            ))
