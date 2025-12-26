"""
Enhanced Job Data Normalization for CamHR - Version 3
Enhanced technical skills detection, education level, and major extraction
"""
import sys
import json
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from extraction.skills_extractor_v3 import EnhancedSkillsExtractor
from extraction.education_extractor_v3 import EnhancedEducationExtractor
from extraction.config import EnhancedExtractionConfig

def load_raw_data(file_path):
    """Load raw job data."""
    print("[*] Loading raw data...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"[+] Loaded {len(data)} jobs")
    return data

def extract_languages(job_langs):
    """Extract language requirements from jobLangs field."""
    results = []
    for jl in job_langs or []:
        try:
            results.append({
                "name": jl["languageId"]["label"].lower(),
                "level": jl["languageLevelId"]["label"].lower()
            })
        except (KeyError, TypeError):
            continue
    return results

def extract_location(raw):
    """Extract location from raw job data."""
    try:
        employer = raw.get("employer", {})
        loc = employer.get("locationId", {}).get("label")
        return loc.lower() if loc else None
    except (AttributeError, TypeError):
        return None

def normalize_job(job, skills_extractor, education_extractor):
    raw = job["raw"]

    # Combine requirement and description for skills extraction
    combined_text = " ".join([
        raw.get("requirement") or "",
        raw.get("description") or ""
    ])

    # Enhanced v3 extraction (better technical skills, education level/major)
    skills = skills_extractor.extract(combined_text)
    education = education_extractor.extract(raw.get("requirement") or "")

    # Extract languages
    languages = extract_languages(raw.get("jobLangs"))

    # Extract location and company
    location = extract_location(raw)
    company = raw.get("employer", {}).get("company")
    industry = raw.get("employer", {}).get("industrialId", {}).get("label")

    # Return same structure as v2
    return {
        "job_id": job["job_id"],
        "job_title": raw.get("title", "").lower(),
        "pubdate": raw.get("pubdate"),
        "expdate": raw.get("expdate"),
        "skills": skills,
        "experience": {
            "min_years": raw.get("workyears", 0),
            "job_title": None
        },
        "education": education,
        "languages": languages,
        "location": location,
        "company": company,
        "industry": industry,
        "raw_text": combined_text.strip()
    }

def save_normalized_data(data, output_path):
    """Save normalized data to JSON."""
    print(f"[*] Saving to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("[+] Save complete!")

def print_statistics(normalized_data):
    """Print extraction statistics."""
    total_jobs = len(normalized_data)
    total_skills = sum(len(job["skills"]) for job in normalized_data)
    avg_skills = total_skills / total_jobs if total_jobs > 0 else 0

    # Education stats
    edu_with_level = sum(1 for job in normalized_data if job["education"].get("level"))
    edu_with_major = sum(1 for job in normalized_data if job["education"].get("major"))

    print("\n" + "="*60)
    print("V3 EXTRACTION STATISTICS")
    print("="*60)
    print(f"Total Jobs Processed:     {total_jobs}")
    print(f"Total Skills Extracted:   {total_skills}")
    print(f"Average Skills per Job:   {avg_skills:.1f}")
    print(f"Education Level Found:    {edu_with_level}/{total_jobs} ({100*edu_with_level/total_jobs:.1f}%)")
    print(f"Education Major Found:    {edu_with_major}/{total_jobs} ({100*edu_with_major/total_jobs:.1f}%)")
    print("="*60)

def print_sample_jobs(normalized_data, num_samples=3):
    """Print sample extraction results."""
    print("\n" + "="*70)
    print(f"SAMPLE RESULTS (showing {min(num_samples, len(normalized_data))} jobs)")
    print("="*70)

    for i, job in enumerate(normalized_data[:num_samples], 1):
        print(f"\nJob {i}: {job['job_id']}")
        print(f"  Title: {job['job_title']}")
        print(f"  Company: {job.get('company', 'N/A')}")
        print(f"  Location: {job.get('location', 'N/A')}")
        print(f"  Skills ({len(job['skills'])}): {', '.join(job['skills'][:10])}{'...' if len(job['skills']) > 10 else ''}")
        print(f"  Education: {job['education'].get('level', 'N/A')} in {job['education'].get('major', 'N/A')}")
        langs = ', '.join([f"{l['name']} ({l['level']})" for l in job.get('languages', [])])
        print(f"  Languages: {langs if langs else 'N/A'}")
        print("-"*70)

def main():
    """Main execution pipeline for v3 enhanced extraction."""
    print("\n" + "="*60)
    print("CAMHR V3 ENHANCED EXTRACTION PIPELINE")
    print("="*60 + "\n")

    # File paths - use the most recent raw data file
    raw_data_dir = Path(__file__).parent.parent / "raw_data"
    raw_files = list(raw_data_dir.glob("camhr_raw_*.json"))
    if not raw_files:
        print(f"[!] No raw data files found in {raw_data_dir}")
        return

    # Use the most recent file
    input_file = max(raw_files, key=lambda f: f.stat().st_mtime)
    print(f"[+] Using raw data file: {input_file.name}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path(__file__).parent / f"camhr_normalized_{timestamp}.json"

    # Load data
    raw_data = load_raw_data(input_file)

    print(f"[*] Testing with first {len(raw_data)} jobs\n")

    # Initialize enhanced extractors
    print("[*] Initializing Enhanced Extraction Engine...")
    config = EnhancedExtractionConfig()
    skills_extractor = EnhancedSkillsExtractor(config)
    education_extractor = EnhancedEducationExtractor(config)
    print()

    # Process jobs
    print("[*] Processing jobs...")
    normalized_data = []
    for i, job in enumerate(raw_data, 1):
        print(f"  Processing job {i}/{len(raw_data)}: {job['job_id']}")
        normalized_job = normalize_job(job, skills_extractor, education_extractor)
        normalized_data.append(normalized_job)

    # Save results
    save_normalized_data(normalized_data, output_file)

    # Print statistics
    print_statistics(normalized_data)
    print_sample_jobs(normalized_data, num_samples=3)

    print(f"\n[+] Extraction complete! Results saved to:")
    print(f"    {output_file}")

if __name__ == "__main__":
    main()
