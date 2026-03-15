"""Scoring tasks — AI-powered job-profile match scoring."""

from app.tasks.celery_app import celery_app


@celery_app.task(bind=True, name="scoring.score_job")
def score_job(self, user_id: str, job_id: str) -> dict:
    """Score a single job against the user's active profile.

    Steps:
    1. Load job and profile from DB
    2. Call scoring_service.score_job()
    3. Update job with score, score_breakdown, confidence, risk_score, decision
    4. Create review queue item if decision == 'review'
    """
    raise NotImplementedError


@celery_app.task(bind=True, name="scoring.bulk_score_jobs")
def bulk_score_jobs(self, user_id: str, job_ids: list[str]) -> dict:
    """Score multiple jobs in batch. Updates progress as each job is scored."""
    raise NotImplementedError
