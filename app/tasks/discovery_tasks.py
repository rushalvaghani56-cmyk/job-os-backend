"""Discovery tasks — scrape job boards and discover new job postings.

Uses Playwright for browser automation. Deduplicates via raw_job.dedup_hash.
"""

from app.tasks.celery_app import celery_app


@celery_app.task(bind=True, name="discovery.discover_jobs")
def discover_jobs(self, user_id: str, profile_id: str) -> dict:
    """Discover new jobs from configured sources for a profile.

    Steps:
    1. Load profile's discovery_config (sources, keywords, locations)
    2. Scrape each source via Playwright or API
    3. Normalize raw job data into RawJob records
    4. Deduplicate against existing jobs using dedup_hash
    5. Create Job records for new, unique postings
    6. Update task progress in tasks table
    """
    raise NotImplementedError
