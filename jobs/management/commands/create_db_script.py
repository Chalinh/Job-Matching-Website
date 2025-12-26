from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path


class Command(BaseCommand):
    help = 'Create a batch script to setup PostgreSQL database automatically'

    def handle(self, *args, **options):
        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']

        # Create Windows batch script
        batch_content = f'''@echo off
REM PostgreSQL Database Setup Script
REM Generated automatically by Django

echo ============================================================
echo PostgreSQL Database Setup
echo ============================================================
echo.
echo Database: {db_name}
echo User: {db_user}
echo Host: {db_host}
echo Port: {db_port}
echo.

echo Enter your PostgreSQL superuser (postgres) password when prompted.
echo.

REM Set PGPASSWORD environment variable (optional - comment out if you prefer manual password entry)
REM set PGPASSWORD=your_postgres_password

echo Creating database...
psql -U postgres -h {db_host} -p {db_port} -c "CREATE DATABASE {db_name};" 2>nul
if %errorlevel% equ 0 (
    echo [OK] Database created
) else (
    echo [INFO] Database may already exist
)

echo Creating user...
psql -U postgres -h {db_host} -p {db_port} -c "CREATE USER {db_user} WITH PASSWORD '{db_password}';" 2>nul
if %errorlevel% equ 0 (
    echo [OK] User created
) else (
    echo [INFO] User may already exist
)

echo Granting privileges...
psql -U postgres -h {db_host} -p {db_port} -c "GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"
psql -U postgres -h {db_host} -p {db_port} -d {db_name} -c "GRANT ALL ON SCHEMA public TO {db_user};"

echo Setting user configuration...
psql -U postgres -h {db_host} -p {db_port} -c "ALTER ROLE {db_user} SET client_encoding TO 'utf8';"
psql -U postgres -h {db_host} -p {db_port} -c "ALTER ROLE {db_user} SET default_transaction_isolation TO 'read committed';"
psql -U postgres -h {db_host} -p {db_port} -c "ALTER ROLE {db_user} SET timezone TO 'UTC';"

echo.
echo ============================================================
echo Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Activate virtual environment: venv\\Scripts\\activate
echo   2. Run migrations: python manage.py migrate
echo   3. Load job data: python manage.py load_jobs
echo   4. Start server: python manage.py runserver
echo.
pause
'''

        # Create PowerShell script as alternative
        powershell_content = f'''# PostgreSQL Database Setup Script
# Generated automatically by Django

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PostgreSQL Database Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Database: {db_name}" -ForegroundColor Yellow
Write-Host "User: {db_user}" -ForegroundColor Yellow
Write-Host "Host: {db_host}" -ForegroundColor Yellow
Write-Host "Port: {db_port}" -ForegroundColor Yellow
Write-Host ""

# Set password for psql (optional)
# $env:PGPASSWORD = "your_postgres_password"

Write-Host "Creating database..." -ForegroundColor Green
psql -U postgres -h {db_host} -p {db_port} -c "CREATE DATABASE {db_name};" 2>$null
if ($?) {{
    Write-Host "[OK] Database created" -ForegroundColor Green
}} else {{
    Write-Host "[INFO] Database may already exist" -ForegroundColor Yellow
}}

Write-Host "Creating user..." -ForegroundColor Green
psql -U postgres -h {db_host} -p {db_port} -c "CREATE USER {db_user} WITH PASSWORD '{db_password}';" 2>$null
if ($?) {{
    Write-Host "[OK] User created" -ForegroundColor Green
}} else {{
    Write-Host "[INFO] User may already exist" -ForegroundColor Yellow
}}

Write-Host "Granting privileges..." -ForegroundColor Green
psql -U postgres -h {db_host} -p {db_port} -c "GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};"
psql -U postgres -h {db_host} -p {db_port} -d {db_name} -c "GRANT ALL ON SCHEMA public TO {db_user};"

Write-Host "Setting user configuration..." -ForegroundColor Green
psql -U postgres -h {db_host} -p {db_port} -c "ALTER ROLE {db_user} SET client_encoding TO 'utf8';"
psql -U postgres -h {db_host} -p {db_port} -c "ALTER ROLE {db_user} SET default_transaction_isolation TO 'read committed';"
psql -U postgres -h {db_host} -p {db_port} -c "ALTER ROLE {db_user} SET timezone TO 'UTC';"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Activate virtual environment: venv\\Scripts\\activate"
Write-Host "  2. Run migrations: python manage.py migrate"
Write-Host "  3. Load job data: python manage.py load_jobs"
Write-Host "  4. Start server: python manage.py runserver"
Write-Host ""
Read-Host "Press Enter to continue"
'''

        # Write batch script
        batch_path = Path(settings.BASE_DIR) / 'setup_database.bat'
        with open(batch_path, 'w', encoding='utf-8') as f:
            f.write(batch_content)

        # Write PowerShell script
        ps_path = Path(settings.BASE_DIR) / 'setup_database.ps1'
        with open(ps_path, 'w', encoding='utf-8') as f:
            f.write(powershell_content)

        self.stdout.write(self.style.SUCCESS(
            '\n✓ Database setup scripts created!'
        ))
        self.stdout.write(f'\n  Batch script: {batch_path}')
        self.stdout.write(f'  PowerShell script: {ps_path}')

        self.stdout.write(self.style.WARNING(
            '\n\nTO RUN (choose one):\n'
        ))
        self.stdout.write(self.style.SUCCESS(
            '  Option 1 (Batch): setup_database.bat'
        ))
        self.stdout.write(self.style.SUCCESS(
            '  Option 2 (PowerShell): powershell -ExecutionPolicy Bypass -File setup_database.ps1'
        ))

        self.stdout.write(self.style.WARNING(
            '\nYou will be prompted for your PostgreSQL superuser (postgres) password.'
        ))

        self.stdout.write(self.style.SUCCESS(
            '\n\nAfter running the script:'
        ))
        self.stdout.write('  1. python manage.py migrate')
        self.stdout.write('  2. python manage.py load_jobs')
        self.stdout.write('  3. python manage.py runserver')
