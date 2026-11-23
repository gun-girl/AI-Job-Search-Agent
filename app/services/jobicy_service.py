
import json
import re
from html import unescape
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from sqlalchemy.orm import Session

from app.models import Job


API_URL = "https://jobicy.com/api/jobs"


def fetch_jobs():
    jobs = []
    cursor = None

    while True:
        params = {
            "count": 100,
            "geo": "europe",
        }

        if cursor:
            params["cursor"] = cursor

        url = f"{API_URL}?{urlencode(params)}"

        request = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "AI-Job-Search-Agent/1.0",
            },
        )

        with urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        if data.get("success") is False:
            raise RuntimeError(data.get("error", "Jobicy API error"))

        jobs.extend(data.get("jobs", []))

        cursor = data.get("nextCursor")

        if not cursor:
            break

    return jobs


def clean_html(value):
    value = re.sub(r"<[^>]+>", " ", value or "")
    return re.sub(r"\s+", " ", unescape(value)).strip()


def classify_category(title, industries, description):
    text = " ".join([
        title or "",
        " ".join(industries or []),
        description or "",
    ]).lower()

    categories = {
        "Cybersecurity": [
            "cybersecurity", "information security",
            "security engineer", "penetration testing",
            "soc analyst",
        ],
        "Artificial Intelligence": [
            "artificial intelligence", "machine learning",
            "deep learning", "generative ai",
            "large language model",
        ],
        "Cloud and DevOps": [
            "devops", "cloud engineer", "aws",
            "azure", "kubernetes", "docker",
            "infrastructure engineer",
        ],
        "Networking": [
            "network engineer", "network administrator",
            "networking", "cisco", "routing", "switching",
        ],
        "IT Support": [
            "it support", "technical support",
            "helpdesk", "help desk", "service desk",
            "application support",
        ],
        "Data": [
            "data engineer", "data analyst",
            "data scientist", "business intelligence",
        ],
        "Business Systems": [
            "business systems", "systems analyst",
            "erp", "system administrator",
        ],
        "Software Development": [
            "software engineer", "software developer",
            "backend", "back-end", "frontend", "front-end",
            "full stack", "full-stack", "programmer",
            "python", "javascript", "typescript",
            "java developer", "php developer",
            "react developer",
        ],
    }

    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in text:
                return category

    # Match standalone AI without matching unrelated words.
    if re.search(r"\bai\b", text):
        return "Artificial Intelligence"

    return None


def classify_experience(level):
    value = (level or "").strip().lower()

    if value in ["any", "all"]:
        return "All"

    if "intern" in value or "trainee" in value:
        return "Trainee"

    if "junior" in value or "entry" in value:
        return "Junior"

    if "senior" in value:
        return "Senior"

    if "mid" in value:
        return "Mid-level"

    return None


def classify_employment(job_types):
    values = " ".join(job_types or []).lower()

    if "internship" in values:
        return "Internship"

    if "part-time" in values:
        return "Part-time"

    if "contract" in values:
        return "Contract"

    if "full-time" in values:
        return "Full-time"

    return None


def safe_salary(value):
    if value is None:
        return None

    try:
        return int(float(value))
    except (ValueError, TypeError):
        return None


def import_jobicy_jobs(db: Session):
    external_jobs = fetch_jobs()

    imported = 0
    skipped = 0

    for item in external_jobs:
        title = (item.get("jobTitle") or "").strip()
        company = (item.get("companyName") or "").strip()
        url = (item.get("url") or "").strip()

        if not title or not company or not url:
            skipped += 1
            continue

        existing = db.query(Job).filter(
            Job.application_url == url
        ).first()

        if existing:
            skipped += 1
            continue

        industries = item.get("jobIndustry") or []
        job_types = item.get("jobType") or []

        description = clean_html(
            item.get("jobDescription")
            or item.get("jobExcerpt")
            or ""
        )

        category = classify_category(
            title,
            industries,
            description,
        )

        # Only import IT-related vacancies.
        if not category:
            skipped += 1
            continue

        geo = (item.get("jobGeo") or "").strip()

        job = Job(
            title=title,
            company=company,
            location=geo or None,
            country=geo or None,
            city=None,
            job_category=category,
            experience_level=classify_experience(
                item.get("jobLevel")
            ),
            employment_type=classify_employment(job_types),
            work_mode="Remote",
            required_languages=[],
            salary_min=safe_salary(item.get("salaryMin")),
            salary_max=safe_salary(item.get("salaryMax")),
            salary_currency=item.get("salaryCurrency"),
            description=description,
            requirements=", ".join(industries + job_types),
            application_url=url,
            source="Jobicy",
        )

        db.add(job)
        imported += 1

    db.commit()

    return {
        "source": "Jobicy",
        "fetched": len(external_jobs),
        "imported": imported,
        "skipped": skipped,
    }
