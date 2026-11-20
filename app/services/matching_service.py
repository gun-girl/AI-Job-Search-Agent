import re

from app.models import CandidateProfile, Job


# Skills the first version of the matching engine can recognise.
# We can expand this list as the project grows.
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
    """Check whether a term appears as a separate word or phrase."""
    pattern = r"(?<!\w)" + re.escape(term).replace(r"\ ", r"\s+") + r"(?!\w)"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def find_job_skills(job_text: str) -> list[str]:
    """Find recognised technical skills in the job text."""
    detected_skills = []

    for skill, aliases in SKILL_ALIASES.items():
        if any(contains_term(job_text, alias) for alias in aliases):
            detected_skills.append(skill)

    return detected_skills


def find_candidate_skills(profile: CandidateProfile) -> list[str]:
    """Convert the candidate's skills into the same recognised skill names."""
    profile_text = " ".join(profile.skills or [])
    candidate_skills = []

    for skill, aliases in SKILL_ALIASES.items():
        if any(contains_term(profile_text, alias) for alias in aliases):
            candidate_skills.append(skill)

    return candidate_skills


def check_title_match(profile: CandidateProfile, job: Job) -> bool:
    """Check whether the job title matches a preferred job title."""
    job_title = (job.title or "").lower()

    for preferred_title in profile.preferred_job_titles or []:
        preferred = preferred_title.lower().strip()

        if preferred and (preferred in job_title or job_title in preferred):
            return True

    return False


def check_experience_match(profile: CandidateProfile, job: Job):
    """
    Compare experience levels when the job explicitly mentions one.
    Return None when there is not enough information.
    """
    job_text = " ".join([
        job.title or "",
        job.description or "",
        job.requirements or ""
    ]).lower()

    junior_terms = [
        "junior", "entry-level", "entry level",
        "intern", "internship", "trainee", "graduate"
    ]

    senior_terms = [
        "senior", "lead developer", "principal",
        "team lead", "manager"
    ]

    job_mentions_junior = any(term in job_text for term in junior_terms)
    job_mentions_senior = any(term in job_text for term in senior_terms)

    candidate_level = (profile.experience_level or "").lower()

    if "junior" in candidate_level:
        if job_mentions_junior:
            return True
        if job_mentions_senior:
            return False

    return None


def match_job_to_profile(profile: CandidateProfile, job: Job) -> dict:
    """Calculate a transparent match score for one job."""
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

    # Only score criteria for which we have information.
    possible_points = 0
    earned_points = 0

    if job_skills:
        possible_points += 70
        earned_points += 70 * (len(matched_skills) / len(job_skills))

    if profile.preferred_job_titles:
        possible_points += 20
        if title_match:
            earned_points += 20

    if experience_match is not None:
        possible_points += 10
        if experience_match:
            earned_points += 10

    score = round((earned_points / possible_points) * 100) if possible_points else 0

    explanations = []

    if matched_skills:
        explanations.append(
            f"Your profile matches {len(matched_skills)} recognised job skill(s)."
        )

    if missing_skills:
        explanations.append(
            f"The job mentions skills not listed in your profile: "
            f"{', '.join(missing_skills)}."
        )

    if title_match:
        explanations.append("The job title matches one of your preferred job titles.")
    elif profile.preferred_job_titles:
        explanations.append("The job title does not match your preferred titles.")

    if experience_match is True:
        explanations.append("The stated experience level appears compatible.")
    elif experience_match is False:
        explanations.append("The stated experience level may not match your profile.")

    if not job_skills:
        explanations.append(
            "No skills from the current recognition list were found in the job text."
        )

    return {
        "job": job,
        "match_score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "title_match": title_match,
        "experience_match": experience_match,
        "explanations": explanations
    }