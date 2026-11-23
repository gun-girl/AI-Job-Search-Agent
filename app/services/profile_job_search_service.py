
import re

from sqlalchemy.orm import Session

from app.models import CandidateProfile, Job


def normalize(value):
    """Normalize text for case-insensitive comparisons."""
    if not value:
        return ""
    return str(value).strip().lower()


def matches_required_filter(job_value, selected_values):
    """
    Check whether a job value matches a profile preference.

    An empty selection means no restriction.
    "All" in the selected values means no restriction.
    A job value of "All" also matches every selected option.
    """
    if not selected_values:
        return True

    selected = {
        normalize(value)
        for value in selected_values
    }

    if "all" in selected:
        return True

    normalized_job_value = normalize(job_value)

    if normalized_job_value == "all":
        return True

    if not normalized_job_value:
        return False

    return normalized_job_value in selected


def matches_location(job, profile):
    """
    Match job location against the candidate's country and city preferences.

    Supported location values:
    - A specific country, such as Finland
    - Europe, for jobs open to candidates across Europe
    - Anywhere, Worldwide, or Global for location-independent jobs

    An empty city preference means all cities in the selected countries.
    """
    countries = {
        normalize(value)
        for value in (profile.preferred_countries or [])
        if normalize(value)
    }

    cities = profile.preferred_cities or []

    # A country must be selected.
    if not countries:
        return False

    job_country = normalize(job.country)

    # A job must have a location or geographic eligibility value.
    if not job_country:
        return False

    # Jobs explicitly open worldwide can match any selected country.
    if job_country in {"anywhere", "worldwide", "global"}:
        country_matches = True

    # Jobs open across Europe can match European country preferences.
    elif job_country == "europe":
        european_countries = {
            "finland",
            "sweden",
            "norway",
            "denmark",
            "iceland",
            "germany",
            "france",
            "spain",
            "italy",
            "netherlands",
            "belgium",
            "austria",
            "ireland",
            "portugal",
            "poland",
            "estonia",
            "latvia",
            "lithuania",
            "luxembourg",
            "greece",
            "czech republic",
            "czechia",
            "romania",
            "bulgaria",
            "croatia",
            "slovakia",
            "slovenia",
            "hungary",
            "cyprus",
            "malta",
            "switzerland",
            "united kingdom",
            "uk",
            "serbia",
            "ukraine",
            "bosnia and herzegovina",
            "montenegro",
            "north macedonia",
            "albania",
            "moldova",
            "monaco",
            "liechtenstein",
            "andorra",
            "san marino",
            "vatican city",
        }

        country_matches = bool(countries & european_countries)

    # Otherwise, compare the specific country.
    else:
        country_matches = job_country in countries

    if not country_matches:
        return False

    # No city preference means all cities in the selected country.
    if not cities:
        return True

    # A job without a specific city cannot satisfy a city restriction.
    if not job.city:
        return False

    return matches_required_filter(job.city, cities)


def matches_it_preferences(job, profile):
    """
    Match jobs using broad IT categories and preferred keywords.

    A job can match either a selected category or at least one keyword.
    """
    categories = profile.preferred_job_categories or []
    keywords = profile.preferred_keywords or []

    job_text = " ".join([
        job.title or "",
        job.job_category or "",
        job.description or "",
        job.requirements or "",
    ]).lower()

    # Check selected job categories.
    selected_categories = {
        normalize(category)
        for category in categories
        if normalize(category)
    }

    category_match = (
        normalize(job.job_category) in selected_categories
        if job.job_category
        else False
    )

    # Check preferred keywords as whole words or phrases.
    keyword_match = False

    for keyword in keywords:
        keyword = normalize(keyword)

        if not keyword:
            continue

        pattern = r"(?<!\w)" + re.escape(keyword) + r"(?!\w)"

        if re.search(pattern, job_text):
            keyword_match = True
            break

    # If no IT preferences were provided, do not restrict by category.
    if not selected_categories and not keywords:
        return True

    return category_match or keyword_match


def job_matches_profile(job, profile):
    """
    Apply all profile filters to a job.

    All required filters must pass. IT category and keyword preferences
    are flexible: matching either one is sufficient.
    """
    if not matches_location(job, profile):
        return False

    if not matches_required_filter(
        job.experience_level,
        profile.experience_levels,
    ):
        return False

    if not matches_required_filter(
        job.employment_type,
        profile.employment_types,
    ):
        return False

    if not matches_required_filter(
        job.work_mode,
        profile.work_modes,
    ):
        return False

    if not matches_it_preferences(job, profile):
        return False

    return True


def search_jobs_for_profile(db: Session, profile_id: int):
    """
    Return all jobs matching a candidate profile.

    Returns:
        None: Profile does not exist.
        list[Job]: Jobs matching the profile's preferences.
    """
    profile = (
        db.query(CandidateProfile)
        .filter(CandidateProfile.id == profile_id)
        .first()
    )

    if not profile:
        return None

    jobs = (
        db.query(Job)
        .order_by(Job.id.desc())
        .all()
    )

    matching_jobs = [
        job
        for job in jobs
        if job_matches_profile(job, profile)
    ]

    return matching_jobs
