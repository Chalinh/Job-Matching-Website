import sqlite3
import json
from datetime import datetime
from pathlib import Path

def create_job_table(cursor):
    """Create the jobs table with all necessary columns"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id VARCHAR(50) NOT NULL,  -- Removed UNIQUE constraint
            job_title VARCHAR(200) NOT NULL,
            company VARCHAR(200) DEFAULT '',
            location VARCHAR(100) DEFAULT '',
            industry VARCHAR(100) DEFAULT '',
            min_years_experience INTEGER DEFAULT 0,
            education_level VARCHAR(50) DEFAULT '',
            education_major VARCHAR(100) DEFAULT '',
            skills TEXT DEFAULT '[]',  -- JSON stored as TEXT in SQLite
            languages TEXT DEFAULT '[]',  -- JSON stored as TEXT in SQLite
            raw_text TEXT DEFAULT '',
            pubdate DATETIME,
            expdate DATETIME,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Create index on job_id for faster lookups
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_id ON jobs(job_id)')

    # Create index on job_title for search
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_job_title ON jobs(job_title)')

    # Create index on location for filtering
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_location ON jobs(location)')

def drop_all_tables(cursor):
    """Drop all tables in the database"""
    # Disable foreign key constraints temporarily
    cursor.execute("PRAGMA foreign_keys = OFF")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        if table_name != 'sqlite_sequence':  # Keep the sequence table
            try:
                cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
                print(f"Dropped table: {table_name}")
            except Exception as e:
                print(f"Error dropping table {table_name}: {e}")

    # Re-enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON")

def load_jobs_from_json(cursor, json_file_path):
    """Load job data from JSON file and insert into database"""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        jobs_data = json.load(f)

    print(f"Loading {len(jobs_data)} jobs from {json_file_path}")

    inserted_count = 0
    for job_data in jobs_data:
        try:
            # Parse dates
            pubdate = None
            expdate = None

            if job_data.get('pubdate'):
                try:
                    # Handle ISO format with timezone
                    pubdate_str = job_data['pubdate'].replace('+0700', '+07:00')
                    pubdate = datetime.fromisoformat(pubdate_str.replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    pass

            if job_data.get('expdate'):
                try:
                    expdate_str = job_data['expdate'].replace('+0700', '+07:00')
                    expdate = datetime.fromisoformat(expdate_str.replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    pass

            # Convert JSON fields to strings
            skills_json = json.dumps(job_data.get('skills', []))
            languages_json = json.dumps(job_data.get('languages', []))

            # Insert job (insert all entries, even with duplicate job_ids)
            cursor.execute('''
                INSERT INTO jobs (
                    job_id, job_title, company, location, industry,
                    min_years_experience, education_level, education_major,
                    skills, languages, raw_text, pubdate, expdate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job_data['job_id'],
                job_data.get('job_title', ''),
                job_data.get('company', ''),
                job_data.get('location', ''),
                job_data.get('industry', ''),
                job_data.get('experience', {}).get('min_years', 0),
                job_data.get('education', {}).get('level', ''),
                job_data.get('education', {}).get('major', ''),
                skills_json,
                languages_json,
                job_data.get('raw_text', ''),
                pubdate,
                expdate
            ))

            inserted_count += 1

        except Exception as e:
            print(f"Error inserting job {job_data.get('job_id', 'unknown')}: {e}")
            continue

    return inserted_count

def main():
    # Database path
    db_path = Path(__file__).parent / 'db.sqlite3'

    # JSON file path - find the most recent normalized data file
    normalized_data_dir = Path(__file__).parent / 'data' / 'normalized_data'
    normalized_files = list(normalized_data_dir.glob("camhr_normalized_*.json"))

    if not normalized_files:
        print(f"Error: No normalized data files found in {normalized_data_dir}")
        return

    # Use the most recent file
    json_file = max(normalized_files, key=lambda f: f.stat().st_mtime)
    print(f"Using normalized data file: {json_file.name}")

    # Connect to database
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()

    try:
        print("Dropping all existing tables...")
        drop_all_tables(cursor)

        print("Creating jobs table...")
        create_job_table(cursor)

        print("Loading job data...")
        inserted_count = load_jobs_from_json(cursor, json_file)

        # Commit changes
        conn.commit()

        print(f"\nSuccess! Inserted {inserted_count} jobs into the database.")

        # Print some statistics
        cursor.execute("SELECT COUNT(*) FROM jobs")
        total_jobs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM jobs WHERE skills != '[]'")
        jobs_with_skills = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM jobs WHERE education_level != ''")
        jobs_with_education = cursor.fetchone()[0]

        print("\nDatabase Statistics:")
        print(f"Total jobs: {total_jobs}")
        print(f"Jobs with skills: {jobs_with_skills}")
        print(f"Jobs with education: {jobs_with_education}")

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()

    finally:
        conn.close()

if __name__ == '__main__':
    main()