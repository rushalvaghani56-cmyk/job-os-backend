"""Scoring service — AI-powered job-profile match scoring.

Uses the scoring weights from Profile.scoring_weights to compute
skill match, seniority match, location match, salary match, and company match.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job
from app.models.profile import Profile


async def score_job(db: AsyncSession, job: Job, profile: Profile) -> dict:
    """Score a single job against a profile. Returns score breakdown dict.

    Steps:
    1. Extract skills from job description (skills_required, skills_preferred)
    2. Compare against user's skills from profile
    3. Apply scoring_weights from profile
    4. Compute composite score, confidence, and risk_score
    5. Determine decision (auto_apply / review / skip) based on automation_config thresholds
    """
    raise NotImplementedError


async def bulk_score_jobs(db: AsyncSession, user_id: uuid.UUID, job_ids: list[uuid.UUID]) -> str:
    """Queue bulk scoring as a Celery task. Returns task_id."""
    raise NotImplementedError
