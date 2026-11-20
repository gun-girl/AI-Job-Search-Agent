import re

from app.models import CandidateProfile, Job


SKILL_ALIASES = {
    "Python": ["python"],
    "FastAPI": ["fastapi"],
    "SQL": ["sql"],
    "Git": ["git"],
    "React": ["react"],
    "TypeScript": ["typescript"],
    "JavaScript": ["javascript"],
    "PHP": ["php"],
    "MySQL": ["mysql"],
    "REST API": ["rest api", "rest apis", "restful api"],
    "Java": ["java"],
    "Node.js": ["node.js", "nodejs"],
    "Docker": ["docker"],
    "AWS": ["aws", "amazon web services"],
    "Azure": ["azure"],
    "Linux": ["linux"],
    "C#": ["c#"],
    ".NET": [".net", "dotnet"],
    "Jira": ["jira"],
}


def contains_term(text: str, term: str) -> bool:
    pattern = (
        r"(?<!\w)"
        + re.escape(term).replace(r"\ ", r"\s+")
        + r"(?!\w)"
    )
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def find_job_skills(job_text: str) -> list[str]:
    detected_skills = []

    for skill, aliases in SKILL_ALIASES.items():
        if any(contains_term(job_text, alias) for alias in aliases):
            detected_skills.append(skill)

    return detected_skills


def find_candidate_skills(profile: CandidateProfile) -> list[str]:
    profile_text = " ".join(profile.skills or [])
    candidate_skills = []

    for skill, aliases in SKILL_ALIASES.items():
        if any(contains_term(profile_text, alias) for alias in aliases):
            candidate_skills.append(skill)

    return candidate_skills


def check_title_match(profile: CandidateProfile, job: Job) -> bool:
    job_title = (job.title or "").lower()

    for preferred_title in profile.preferred_job_titles or []:
        preferred = preferred_title.lower().strip()

        if preferred and (
            preferred in job_title or job_title in preferred
        ):
            return True

    return False


def check_experience_match(profile: CandidateProfile, job: Job):
    candidate_level = (profile.experience_level or "").lower().strip()
    job_level = (job.experience_level or "").lower().strip()

    if not candidate_level or not job_level:
        return None

    junior_levels = {"junior", "entry-level", "entry level", "graduate"}
    mid_levels = {"mid", "mid-level", "intermediate"}
    senior_levels = {"senior", "lead", "principal"}

    if candidate_level == job_level:
        return True

    if candidate_level in junior_levels and job_level in junior_levels:
        return True

    if candidate_level in mid_levels and job_level in mid_levels:
        return True

    if candidate_level in senior_levels and job_level in senior_levels:
        return True

    return False


def check_preference_match(
    preferences: list[str] | None,
    job_value: str | None
):
    if not preferences or not job_value:
        return None

    normalised_preferences = {
        value.strip().lower() for value in preferences
    }

    return job_value.strip().lower() in normalised_preferences


def check_language_match(profile: CandidateProfile, job: Job):
    candidate_languages = profile.languages or []
    required_languages = job.required_languages or []

    if not candidate_languages or not required_languages:
        return None, [], []

    # "English (Fluent)" becomes "english"
    candidate_language_names = {
        language.split("(")[0].strip().lower()
        for language in candidate_languages
    }

    matched = [
        language for language in required_languages
        if language.strip().lower() in candidate_language_names
    ]

    missing = [
        language for language in required_languages
        if language.strip().lower() not in candidate_language_names
    ]

    return len(missing) == 0, matched, missing


def check_salary_match(profile: CandidateProfile, job: Job):
    candidate_has_salary = (
        profile.salary_min is not None
        or profile.salary_max is not None
    )

    job_has_salary = (
        job.salary_min is not None
        or job.salary_max is not None
    )

    if not candidate_has_salary or not job_has_salary:
        return None

    # Compare the ranges when both sides provide them.
    candidate_min = profile.salary_min or 0
    candidate_max = (
        profile.salary_max
        if profile.salary_max is not None
        else float("inf")
    )

    job_min = job.salary_min or 0
    job_max = (
        job.salary_max
        if job.salary_max is not None
        else float("inf")
    )

    return max(candidate_min, job_min) <= min(candidate_max, job_max)


def match_job_to_profile(profile: CandidateProfile, job: Job) -> dict:
    job_text = " ".join([
        job.title or "",
        job.description or "",
        job.requirements or ""
    ]).lower()

    job_skills = find_job_skills(job_text)
    candidate_skills = find_candidate_skills(profile)

    matched_skills = [
        skill for skill in job_skills
        if skill in candidate_skills
    ]

    missing_skills = [
        skill for skill in job_skills
        if skill not in candidate_skills
    ]

    title_match = check_title_match(profile, job)
    experience_match = check_experience_match(profile, job)

    employment_type_match = check_preference_match(
        profile.employment_types,
        job.employment_type
    )

    work_mode_match = check_preference_match(
        profile.work_modes,
        job.work_mode
    )

    language_match, matched_languages, missing_languages = (
        check_language_match(profile, job)
    )

    salary_match = check_salary_match(profile, job)

    # Each criterion contributes only when enough information exists.
    criteria = [
        (40, len(matched_skills) / len(job_skills) if job_skills else None),
        (15, 1 if title_match else 0 if profile.preferred_job_titles else None),
        (10, 1 if experience_match else 0 if experience_match is False else None),
        (10, 1 if employment_type_match else 0 if employment_type_match is False else None),
        (10, 1 if work_mode_match else 0 if work_mode_match is False else None),
        (10, 1 if language_match else 0 if language_match is False else None),
        (5, 1 if salary_match else 0 if salary_match is False else None),
    ]

    possible_points = sum(
        weight for weight, result in criteria
        if result is not None
    )

    earned_points = sum(
        weight * result for weight, result in criteria
        if result is not None
    )

    score = (
        round(earned_points / possible_points * 100)
        if possible_points else 0
    )

    explanations = []

    if job_skills:
        explanations.append(
            f"You match {len(matched_skills)} of "
            f"{len(job_skills)} recognised technical skills."
        )
    else:
        explanations.append(
            "No recognised technical skills were found in the job text."
        )

    if missing_skills:
        explanations.append(
            f"Skills not listed in your profile: {', '.join(missing_skills)}."
        )

    if profile.preferred_job_titles:
        explanations.append(
            "The job title matches your preferences."
            if title_match else
            "The job title does not match your preferred titles."
        )

    if experience_match is not None:
        explanations.append(
            "The experience levels are compatible."
            if experience_match else
            "The experience levels do not match."
        )

    if employment_type_match is not None:
        explanations.append(
            "The employment type matches your preferences."
            if employment_type_match else
            "The employment type does not match your preferences."
        )

    if work_mode_match is not None:
        explanations.append(
            "The work mode matches your preferences."
            if work_mode_match else
            "The work mode does not match your preferences."
        )

    if language_match is not None:
        explanations.append(
            "All listed required languages are in your profile."
            if language_match else
            f"Languages not listed in your profile: "
            f"{', '.join(missing_languages)}."
        )

    if salary_match is not None:
        explanations.append(
            "The salary range overlaps your target."
            if salary_match else
            "The salary range does not overlap your target."
        )

    return {
        "job": job,
        "match_score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "title_match": title_match,
        "experience_match": experience_match,
        "employment_type_match": employment_type_match,
        "work_mode_match": work_mode_match,
        "language_match": language_match,
        "matched_languages": matched_languages,
        "missing_languages": missing_languages,
        "salary_match": salary_match,
        "explanations": explanations
    }