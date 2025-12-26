import requests
import json
import time
from datetime import datetime

BASE_URL = "https://api.camhr.com/v1.0.0"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

DELAY = 2


def get_total_pages():
    url = f"{BASE_URL}/jobs/simple/page-query?page=1&size=10&locationId=0&jobTitleOrCompany="
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()["data"]["totalPage"]


def get_job_ids(page):
    url = f"{BASE_URL}/jobs/simple/page-query?page={page}&size=10&locationId=0&jobTitleOrCompany="
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return [job["id"] for job in res.json()["data"]["result"]]


def get_job_raw(job_id):
    url = f"{BASE_URL}/jobs/{job_id}"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        print(f"❌ Failed job {job_id}")
        return None

    data = res.json().get("data", {})

    return {
        "pubdate": data.get("pubdate"),
        "expdate": data.get("expdate"),
        "title": data.get("title"),
        "hirelings": data.get("hirelings"),
        "workyears": data.get("workyears"),
        "address": data.get("address"),
        "requirement": data.get("requirement"),
        "description": data.get("description"),
        "jobLangs": data.get("jobLangs"),
        "employer": data.get("employer"),
    }


def scrape_raw_camhr():
    total_pages = get_total_pages()
    print(f"🔎 Total pages: {total_pages}")

    raw_jobs = []

    # 👇 EXACTLY page=1 → page=totalPage
    for page in range(1, total_pages + 1):
        print(f"📄 Scraping page {page}/{total_pages}")

        job_ids = get_job_ids(page)

        for job_id in job_ids:
            raw = get_job_raw(job_id)
            if raw:
                raw_jobs.append({
                    "page": page,
                    "job_id": job_id,
                    "raw": raw
                })
            time.sleep(DELAY)

    save_raw(raw_jobs)
    return raw_jobs


def save_raw(data):
    filename = f"../raw_data/camhr_raw_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(data)} jobs → {filename}")


if __name__ == "__main__":
    scrape_raw_camhr()
